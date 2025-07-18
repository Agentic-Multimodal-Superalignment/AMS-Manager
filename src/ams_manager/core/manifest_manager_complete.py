#!/usr/bin/env python3
"""
🧙‍♂️ Manifest Manager - Dynamic Tool Discovery and Configuration

This module handles:
- Multiple manifest types (GitHub, HuggingFace, custom)
- Auto-discovery of installation instructions
- Manifest export/import for sharing
- Dynamic configuration generation using Open Interpreter
- Ollama model management and integration
- Documentation querying for installed projects
"""

import json
import yaml
import re
import requests
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, asdict
from enum import Enum

try:
    from interpreter import interpreter
    INTERPRETER_AVAILABLE = True
except ImportError:
    INTERPRETER_AVAILABLE = False
    interpreter = None


class SourceType(Enum):
    GITHUB = "github"
    HUGGINGFACE = "huggingface"
    CUSTOM = "custom"
    PYPI = "pypi"


@dataclass
class OllamaModel:
    """Represents an Ollama model"""
    name: str
    parameter_size: str
    size_gb: float
    family: str = "unknown"
    
    @classmethod
    def from_ollama_info(cls, model_name: str, info: dict) -> "OllamaModel":
        """Create OllamaModel from Ollama API response"""
        # Extract size in GB from bytes
        size_bytes = info.get('size', 0)
        size_gb = round(size_bytes / (1024**3), 1) if size_bytes else 0.0
        
        # Extract parameter info from model name or details
        param_size = "unknown"
        if ':' in model_name:
            param_size = model_name.split(':')[-1]
        
        family = info.get('details', {}).get('family', 'unknown')
        
        return cls(
            name=model_name,
            parameter_size=param_size,
            size_gb=size_gb,
            family=family
        )


@dataclass
class ToolConfig:
    name: str
    display_name: str
    source_type: SourceType
    url: str
    description: str = ""
    install_commands: List[str] = None
    start_command: str = ""
    web_interface: str = ""
    gui_mode: bool = False
    requirements_file: str = "requirements.txt"
    python_version: str = ">=3.8"
    use_uv: bool = True
    use_venv: bool = True
    folder_name: str = ""
    auto_configured: bool = False
    
    def __post_init__(self):
        if self.install_commands is None:
            self.install_commands = []
        if not self.folder_name:
            self.folder_name = self.name


class OllamaManager:
    """Manages Ollama interactions"""
    
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
        self.default_model = None
        self.session_model = None
        
    def is_available(self) -> bool:
        """Check if Ollama is running"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def list_models(self) -> List[OllamaModel]:
        """List available models"""
        if not self.is_available():
            return []
        
        try:
            response = requests.get(f"{self.base_url}/api/tags")
            if response.status_code == 200:
                models_data = response.json()
                models = []
                for model_info in models_data.get('models', []):
                    model = OllamaModel.from_ollama_info(
                        model_info['name'], 
                        model_info
                    )
                    models.append(model)
                return models
        except Exception as e:
            print(f"Error listing models: {e}")
        return []
    
    def configure_interpreter(self, model_name: str, temperature: float = 0.1):
        """Configure Open Interpreter with Ollama model"""
        if not INTERPRETER_AVAILABLE:
            return False
        
        try:
            interpreter.offline = True
            interpreter.llm.model = model_name
            interpreter.llm.api_key = "fake_key"
            interpreter.llm.api_base = self.base_url
            interpreter.llm.temperature = temperature
            
            self.session_model = model_name
            return True
        except Exception as e:
            print(f"Error configuring interpreter: {e}")
            return False
    
    def hot_swap_model(self, model_name: str, temperature: float = None) -> bool:
        """Hot swap to a different model during session"""
        if temperature is None:
            temperature = getattr(interpreter.llm, 'temperature', 0.1) if INTERPRETER_AVAILABLE else 0.1
        
        return self.configure_interpreter(model_name, temperature)
    
    def get_recommended_models(self) -> Dict[str, List[str]]:
        """Get recommended models by use case"""
        models = self.list_models()
        if not models:
            return {}
        
        recommendations = {
            "coding": [],
            "general": [],
            "fast": [],
            "creative": [],
            "reasoning": []
        }
        
        for model in models:
            name = model.name.lower()
            
            # Coding models
            if any(keyword in name for keyword in ["coder", "code", "opencoder", "qwen2.5-coder"]):
                recommendations["coding"].append(model.name)
            
            # Fast/lightweight models
            if model.size_gb < 2.0 or "1b" in model.parameter_size.lower():
                recommendations["fast"].append(model.name)
            
            # Creative models
            if any(keyword in name for keyword in ["creative", "dolphin", "uncensored"]):
                recommendations["creative"].append(model.name)
            
            # Reasoning models
            if any(keyword in name for keyword in ["deepseek-r1", "marco-o1", "reasoning"]):
                recommendations["reasoning"].append(model.name)
            
            # General purpose
            if any(keyword in name for keyword in ["llama3", "gemma", "phi", "granite"]):
                recommendations["general"].append(model.name)
        
        return {k: v[:5] for k, v in recommendations.items() if v}  # Top 5 each
    
    def query_model(self, prompt: str, model_name: str = None) -> str:
        """Query a model directly via Ollama API"""
        model = model_name or self.session_model or self.default_model
        if not model:
            return "No model configured"
        
        try:
            payload = {
                "model": model,
                "prompt": prompt,
                "stream": False
            }
            response = requests.post(f"{self.base_url}/api/generate", json=payload)
            if response.status_code == 200:
                return response.json().get('response', 'No response')
        except Exception as e:
            return f"Error querying model: {e}"


class ProjectDocsQuerier:
    """Queries project documentation using Ollama"""
    
    def __init__(self, aiml_home: Path, ollama_manager: OllamaManager):
        self.aiml_home = Path(aiml_home)
        self.ollama_manager = ollama_manager
        self.docs_cache = {}
    
    def extract_readme_content(self, project_path: Path) -> str:
        """Extract README content from a project"""
        readme_files = ['README.md', 'README.rst', 'README.txt', 'readme.md']
        
        for readme_file in readme_files:
            readme_path = project_path / readme_file
            if readme_path.exists():
                try:
                    with open(readme_path, 'r', encoding='utf-8', errors='ignore') as f:
                        return f.read()
                except:
                    continue
        return ""
    
    def extract_install_instructions(self, readme_content: str) -> List[str]:
        """Extract installation instructions from README using Ollama"""
        if not readme_content.strip():
            return []
        
        prompt = f"""
        Analyze this README and extract installation commands. Focus on:
        1. pip/uv install commands
        2. git clone commands  
        3. Environment setup (venv, conda)
        4. Requirements installation
        5. Post-install setup commands
        
        Return only the commands as a JSON array of strings.
        
        README Content:
        {readme_content[:3000]}
        """
        
        response = self.ollama_manager.query_model(prompt)
        
        try:
            # Extract JSON from response
            json_match = re.search(r'\[.*\]', response, re.DOTALL)
            if json_match:
                commands = json.loads(json_match.group())
                return [cmd for cmd in commands if isinstance(cmd, str)]
        except:
            pass
        
        return []
    
    def query_project_docs(self, project_name: str, question: str) -> str:
        """Query documentation for a specific project"""
        project_paths = [
            self.aiml_home / project_name,
            self.aiml_home / "github" / project_name,
            self.aiml_home / "huggingface" / project_name,
            self.aiml_home / "custom" / project_name
        ]
        
        # Find the project
        project_path = None
        for path in project_paths:
            if path.exists():
                project_path = path
                break
        
        if not project_path:
            return f"Project {project_name} not found"
        
        # Get documentation
        readme_content = self.extract_readme_content(project_path)
        
        if not readme_content:
            return f"No documentation found for {project_name}"
        
        prompt = f"""
        Based on the documentation for {project_name}, answer this question: {question}
        
        Documentation:
        {readme_content[:4000]}
        
        Please provide a helpful and accurate answer based on the documentation.
        """
        
        return self.ollama_manager.query_model(prompt)


class ManifestManager:
    """🧙‍♂️ Intelligent Manifest Management System"""
    
    def __init__(self, aiml_home: Path):
        self.aiml_home = Path(aiml_home)
        self.manifests_dir = self.aiml_home / "manifests"
        self.manifests_dir.mkdir(exist_ok=True)
        
        # Source-specific directories
        self.github_dir = self.aiml_home / "github"
        self.huggingface_dir = self.aiml_home / "huggingface"
        self.custom_dir = self.aiml_home / "custom"
        
        for dir_path in [self.github_dir, self.huggingface_dir, self.custom_dir]:
            dir_path.mkdir(exist_ok=True)
        
        # Initialize Ollama and docs querying
        self.ollama_manager = OllamaManager()
        self.docs_querier = ProjectDocsQuerier(aiml_home, self.ollama_manager)
    
    def get_source_directory(self, source_type: SourceType) -> Path:
        """Get the appropriate directory for a source type"""
        mapping = {
            SourceType.GITHUB: self.github_dir,
            SourceType.HUGGINGFACE: self.huggingface_dir,
            SourceType.CUSTOM: self.custom_dir,
            SourceType.PYPI: self.custom_dir
        }
        return mapping.get(source_type, self.custom_dir)
    
    def create_manifest(self, name: str, tools: List[ToolConfig]) -> Dict[str, Any]:
        """Create a new manifest with tools"""
        manifest = {
            "metadata": {
                "name": name,
                "version": "1.0.0",
                "created_by": "Merlin 🧙‍♂️",
                "description": f"Custom manifest: {name}",
                "source_types": list(set(tool.source_type.value for tool in tools))
            },
            "tools": [asdict(tool) for tool in tools],
            "notes": {
                "auto_generated": True,
                "modular_structure": "Supports GitHub, HuggingFace, and custom sources",
                "wizard_note": "🧙‍♂️ Dynamically configured with AI assistance!"
            }
        }
        return manifest
    
    def save_manifest(self, manifest: Dict[str, Any], filename: str = None) -> Path:
        """Save manifest to file"""
        if not filename:
            filename = f"{manifest['metadata']['name']}.json"
        
        manifest_path = self.manifests_dir / filename
        with open(manifest_path, 'w', encoding='utf-8') as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)
        
        return manifest_path
    
    def load_manifest(self, manifest_path: Union[str, Path]) -> Dict[str, Any]:
        """Load manifest from file"""
        path = Path(manifest_path)
        if not path.is_absolute():
            path = self.manifests_dir / path
        
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def list_manifests(self) -> List[Dict[str, Any]]:
        """List all available manifests"""
        manifests = []
        for manifest_file in self.manifests_dir.glob("*.json"):
            try:
                manifest = self.load_manifest(manifest_file)
                manifests.append({
                    "file": manifest_file.name,
                    "name": manifest["metadata"]["name"],
                    "description": manifest["metadata"].get("description", ""),
                    "tools_count": len(manifest.get("tools", [])),
                    "source_types": manifest["metadata"].get("source_types", [])
                })
            except Exception as e:
                print(f"⚠️ Error loading {manifest_file}: {e}")
        return manifests
    
    def auto_configure_tool(self, url: str, name: str = None) -> Optional[ToolConfig]:
        """🧙‍♂️ Auto-configure a tool using Open Interpreter to read README"""
        print(f"🧙‍♂️ Auto-configuring tool from: {url}")
        
        # Determine source type
        source_type = self._detect_source_type(url)
        
        # Extract name if not provided
        if not name:
            name = url.split('/')[-1].replace('.git', '')
        
        # Use Ollama or fallback to basic configuration
        if self.ollama_manager.is_available():
            config = self._auto_configure_with_ollama(url, name, source_type)
            if config:
                return config
        
        # Fallback to basic configuration
        return ToolConfig(
            name=name,
            display_name=name.title(),
            source_type=source_type,
            url=url,
            description=f"Tool from {source_type.value}",
            auto_configured=False
        )
    
    def _auto_configure_with_ollama(self, url: str, name: str, source_type: SourceType) -> Optional[ToolConfig]:
        """Auto-configure using Ollama to analyze README"""
        prompt = f"""
        Analyze this repository and extract installation information: {url}
        
        Please provide:
        1. Display name and description
        2. Installation commands (prefer UV if possible, fall back to pip)
        3. Start/run commands
        4. Web interface URL if it's a web app
        5. Whether it needs a virtual environment
        6. Python version requirements
        
        Return as JSON with these keys:
        - display_name
        - description  
        - install_commands (array)
        - start_command
        - web_interface
        - use_venv (boolean)
        - python_version
        
        Focus on the README.md and setup instructions.
        """
        
        try:
            response = self.ollama_manager.query_model(prompt)
            
            # Extract JSON from response
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                config_data = json.loads(json_match.group(0))
                
                # Create ToolConfig
                tool_config = ToolConfig(
                    name=name,
                    display_name=config_data.get('display_name', name),
                    source_type=source_type,
                    url=url,
                    description=config_data.get('description', ''),
                    install_commands=config_data.get('install_commands', []),
                    start_command=config_data.get('start_command', ''),
                    web_interface=config_data.get('web_interface', ''),
                    use_venv=config_data.get('use_venv', True),
                    python_version=config_data.get('python_version', '>=3.8'),
                    auto_configured=True
                )
                
                print(f"✅ Auto-configured {tool_config.display_name}")
                return tool_config
                
        except Exception as e:
            print(f"⚠️ Auto-configuration failed: {e}")
        
        return None
    
    def _detect_source_type(self, url: str) -> SourceType:
        """Detect the source type from URL"""
        if 'github.com' in url:
            return SourceType.GITHUB
        elif 'huggingface.co' in url:
            return SourceType.HUGGINGFACE
        else:
            return SourceType.CUSTOM
    
    def export_manifests(self, export_path: Path, manifest_names: List[str] = None) -> Path:
        """Export manifests as a shareable package"""
        export_data = {
            "metadata": {
                "exported_by": "Merlin 🧙‍♂️",
                "export_version": "1.0.0",
                "total_manifests": 0,
                "total_tools": 0
            },
            "manifests": {}
        }
        
        manifests_to_export = manifest_names or [f.stem for f in self.manifests_dir.glob("*.json")]
        
        for manifest_name in manifests_to_export:
            try:
                manifest = self.load_manifest(f"{manifest_name}.json")
                export_data["manifests"][manifest_name] = manifest
                export_data["metadata"]["total_manifests"] += 1
                export_data["metadata"]["total_tools"] += len(manifest.get("tools", []))
            except Exception as e:
                print(f"⚠️ Failed to export {manifest_name}: {e}")
        
        with open(export_path, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        print(f"📦 Exported {export_data['metadata']['total_manifests']} manifests with {export_data['metadata']['total_tools']} tools")
        return export_path
    
    def import_manifests(self, import_path: Path, overwrite: bool = False) -> List[str]:
        """Import manifests from a shareable package"""
        with open(import_path, 'r', encoding='utf-8') as f:
            import_data = json.load(f)
        
        imported_manifests = []
        
        for manifest_name, manifest_data in import_data.get("manifests", {}).items():
            manifest_file = self.manifests_dir / f"{manifest_name}.json"
            
            if manifest_file.exists() and not overwrite:
                print(f"⚠️ Manifest {manifest_name} already exists, skipping")
                continue
            
            with open(manifest_file, 'w', encoding='utf-8') as f:
                json.dump(manifest_data, f, indent=2, ensure_ascii=False)
            
            imported_manifests.append(manifest_name)
            print(f"✅ Imported manifest: {manifest_name}")
        
        return imported_manifests
    
    # Ollama integration methods
    def list_ollama_models(self) -> List[OllamaModel]:
        """List available Ollama models"""
        return self.ollama_manager.list_models()
    
    def configure_model(self, model_name: str = "llama3.1:latest", 
                       temperature: float = 0.1) -> bool:
        """Configure Open Interpreter with an Ollama model"""
        return self.ollama_manager.configure_interpreter(model_name, temperature)
    
    def hot_swap_model(self, model_name: str, temperature: float = None) -> bool:
        """Hot swap to a different model during session"""
        return self.ollama_manager.hot_swap_model(model_name, temperature)
    
    def get_model_recommendations(self) -> Dict[str, List[str]]:
        """Get recommended models by use case"""
        return self.ollama_manager.get_recommended_models()
    
    def show_model_status(self) -> None:
        """Show current model configuration and available models"""
        if not self.ollama_manager.is_available():
            print("❌ Ollama is not running")
            return
        
        print("🦙 Ollama Model Status:")
        
        # Current model info if interpreter is configured
        if INTERPRETER_AVAILABLE and hasattr(interpreter.llm, 'model'):
            current_model = getattr(interpreter.llm, 'model', 'Not configured')
            temp = getattr(interpreter.llm, 'temperature', 'Not set')
            print(f"  📊 Current model: {current_model}")
            print(f"  🌡️ Temperature: {temp}")
        
        # Show available models
        models = self.list_ollama_models()
        if models:
            print(f"  📚 Available models: {len(models)}")
            for model in models[:5]:  # Show top 5
                print(f"    • {model.name} ({model.parameter_size}, {model.size_gb}GB)")
        else:
            print("  ❌ No models found")
    
    # Documentation querying methods
    def query_project_documentation(self, project_name: str, question: str) -> str:
        """Query documentation for a specific project"""
        return self.docs_querier.query_project_docs(project_name, question)
    
    def list_available_projects(self) -> List[str]:
        """List all projects that have documentation available"""
        projects = set()
        
        # Scan all directories in the AI projects folder
        for root_dir in [self.aiml_home, self.github_dir, self.huggingface_dir, self.custom_dir]:
            if root_dir.exists():
                for item in root_dir.iterdir():
                    if item.is_dir() and not item.name.startswith('.'):
                        # Check if it has any documentation
                        readme_files = list(item.glob("README*")) + list(item.glob("readme*"))
                        if readme_files or (item / "docs").exists():
                            projects.add(item.name)
        
        return sorted(list(projects))
