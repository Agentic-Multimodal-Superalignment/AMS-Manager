#!/usr/bin/env python3
"""
🧙‍♂️ Manifest Manager - Dynamic Tool Discovery and Configuration

This module handles:
- Multiple manifest types (GitHub, HuggingFace, custom)
- Auto-discovery of installation instructions
- Manifest export/import for sharing
- Dynamic configuration generation using Open Interpreter
- Olloma model management and integration
- Documentation querying for installed projects
"""

import json
import yaml
import re
import requests
import subprocess
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, asdict
from enum import Enum
from datetime import datetime

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
    name: str
    parameter_size: str
    size_gb: float
    family: str = "unknown"


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

    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization"""
        return {
            "name": self.name,
            "display_name": self.display_name,
            "source_type": self.source_type.value,
            "url": self.url,
            "description": self.description,
            "install_commands": self.install_commands,
            "start_command": self.start_command,
            "web_interface": self.web_interface,
            "use_venv": self.use_venv,
            "python_version": self.python_version,
            "requirements_file": self.requirements_file,
            "auto_configured": self.auto_configured
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'ToolConfig':
        """Create ToolConfig from dictionary"""
        return cls(
            name=data["name"],
            display_name=data.get("display_name", data["name"]),
            source_type=SourceType(data["source_type"]),
            url=data.get("url", ""),
            description=data.get("description", ""),
            install_commands=data.get("install_commands", []),
            start_command=data.get("start_command", ""),
            web_interface=data.get("web_interface", ""),
            use_venv=data.get("use_venv", True),
            python_version=data.get("python_version", ">=3.8"),
            requirements_file=data.get("requirements_file", "requirements.txt"),
            auto_configured=data.get("auto_configured", False)
        )


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
            
        # Configure Open Interpreter with Ollama
        self.configure_interpreter()
    
    def configure_interpreter(self):
        """Configure Open Interpreter to use Ollama properly"""
        if INTERPRETER_AVAILABLE and interpreter:
            try:
                # Configure for Ollama according to Open Interpreter docs
                interpreter.offline = True  # Disables online features
                interpreter.llm.api_base = "http://localhost:11434/v1"  # Ollama OpenAI-compatible endpoint
                interpreter.llm.api_key = "not-needed"  # Required by LiteLLM but not used
                interpreter.auto_run = False  # Always ask for confirmation
                
                # Set context window and tokens for local models
                interpreter.llm.context_window = 8000
                interpreter.llm.max_tokens = 1000
                
                # Get available models and set preferred one
                models = self.list_ollama_models()
                if models:
                    # Prefer coding-friendly models - use actual available model names
                    preferred_models = ['qwen2.5-coder', 'deepseek', 'codellama', 'opencoder', 'llama3.1']
                    selected_model = None
                    
                    for pref in preferred_models:
                        for model in models:
                            if pref in model.name.lower():
                                selected_model = model.name
                                break
                        if selected_model:
                            break
                    
                    # Use selected model or fallback to first available
                    if not selected_model and models:
                        selected_model = models[0].name
                    
                    if selected_model:
                        # Use OpenAI compatible format - this is the key fix!
                        model_name = selected_model.replace(':latest', '')  # Remove :latest tag
                        interpreter.llm.model = f"openai/{model_name}"
                        print(f"🦙 Using Ollama model: {interpreter.llm.model}")
                        
                        # Test connection
                        print("🔧 Testing Ollama connection...")
                        try:
                            # Simple test
                            test_result = interpreter.chat("Say 'OK'", display=False, stream=False)
                            print("✅ Ollama configuration complete and tested!")
                        except Exception as test_e:
                            print(f"⚠️ Ollama test failed: {test_e}")
                            
            except Exception as e:
                print(f"⚠️ Failed to configure Ollama: {e}")
    
    def list_ollama_models(self) -> List[OllamaModel]:
        """List available Ollama models"""
        try:
            result = subprocess.run(['ollama', 'list'], capture_output=True, text=True)
            if result.returncode != 0:
                return []
            
            models = []
            lines = result.stdout.strip().split('\n')[1:]  # Skip header
            for line in lines:
                if line.strip():
                    parts = line.split()
                    if len(parts) >= 3:
                        name = parts[0]
                        size_str = parts[2]
                        # Extract size in GB
                        size_gb = 0.0
                        if 'GB' in size_str:
                            size_gb = float(re.findall(r'[\d.]+', size_str)[0])
                        elif 'MB' in size_str:
                            size_gb = float(re.findall(r'[\d.]+', size_str)[0]) / 1024
                        
                        # Determine parameter size and family
                        param_size = "unknown"
                        family = "unknown"
                        
                        name_lower = name.lower()
                        if 'llama' in name_lower:
                            family = "llama"
                        elif 'codellama' in name_lower:
                            family = "codellama"
                        elif 'qwen' in name_lower:
                            family = "qwen"
                        elif 'deepseek' in name_lower:
                            family = "deepseek"
                        elif 'mistral' in name_lower:
                            family = "mistral"
                        
                        # Extract parameter size from name
                        if ':' in name:
                            param_size = name.split(':')[1]
                        elif 'b' in name_lower:
                            param_match = re.search(r'(\d+\.?\d*)b', name_lower)
                            if param_match:
                                param_size = f"{param_match.group(1)}B"
                        
                        models.append(OllamaModel(
                            name=name,
                            parameter_size=param_size,
                            size_gb=size_gb,
                            family=family
                        ))
            
            return models
        except Exception as e:
            print(f"⚠️ Error listing Ollama models: {e}")
            return []
    
    def configure_model(self, model_name: str, temperature: float = 0.1) -> bool:
        """Configure default model for Open Interpreter"""
        if not INTERPRETER_AVAILABLE:
            print("❌ Open Interpreter not available")
            return False
        
        try:
            # Use OpenAI compatible format for Ollama models
            model_name = model_name.replace(':latest', '')  # Remove tag if present
            interpreter.llm.model = f"openai/{model_name}"
            interpreter.llm.temperature = temperature
            return True
        except Exception as e:
            print(f"❌ Failed to configure model: {e}")
            return False
    
    def hot_swap_model(self, model_name: str, temperature: Optional[float] = None) -> bool:
        """Hot-swap to a different model for the current session"""
        if not INTERPRETER_AVAILABLE:
            print("❌ Open Interpreter not available")
            return False
        
        try:
            # Use OpenAI compatible format for Ollama models
            model_name = model_name.replace(':latest', '')  # Remove tag if present
            interpreter.llm.model = f"openai/{model_name}"
            if temperature is not None:
                interpreter.llm.temperature = temperature
            print(f"🔄 Hot-swapped to openai/{model_name}")
            return True
        except Exception as e:
            print(f"❌ Failed to hot-swap model: {e}")
            return False
    
    def show_model_status(self):
        """Show current model configuration"""
        if not INTERPRETER_AVAILABLE:
            print("❌ Open Interpreter not available")
            return
        
        print(f"🤖 Current Model: {getattr(interpreter.llm, 'model', 'Not set')}")
        print(f"🌡️ Temperature: {getattr(interpreter.llm, 'temperature', 'Not set')}")
        print(f"🔗 API Base: {getattr(interpreter.llm, 'api_base', 'Not set')}")
        print(f"🔄 Offline Mode: {getattr(interpreter, 'offline', False)}")
    
    def get_model_recommendations(self) -> Dict[str, List[str]]:
        """Get model recommendations by use case"""
        models = self.list_ollama_models()
        if not models:
            return {}
        
        recommendations = {
            "coding": [],
            "documentation": [],
            "general": [],
            "fast": []
        }
        
        for model in models:
            model_lower = model.name.lower()
            
            # Coding models
            if any(term in model_lower for term in ['code', 'coder', 'codellama']):
                recommendations["coding"].append(model.name)
            
            # Documentation/text models
            if any(term in model_lower for term in ['llama', 'qwen', 'mistral']):
                recommendations["documentation"].append(model.name)
            
            # General purpose
            if model.size_gb > 3:  # Larger models for general use
                recommendations["general"].append(model.name)
            
            # Fast models (smaller)
            if model.size_gb < 5:
                recommendations["fast"].append(model.name)
        
        return recommendations
    
    def auto_configure_tool(self, url: str, name: str = None) -> Optional[ToolConfig]:
        """🧙‍♂️ Auto-configure a tool using Open Interpreter to read README"""
        if not INTERPRETER_AVAILABLE:
            print("❌ Open Interpreter not available for auto-configuration")
            return None
        
        print(f"🧙‍♂️ Auto-configuring tool from: {url}")
        
        # Determine source type
        source_type = self._detect_source_type(url)
        
        # Extract name if not provided
        if not name:
            name = url.split('/')[-1].replace('.git', '')
        
        # Use Open Interpreter to analyze the repository
        analysis_prompt = f"""
        Analyze this repository and extract installation information: {url}
        
        Please visit the repository, read the README.md and any setup/installation documentation.
        
        Provide installation details in JSON format with these keys:
        - display_name: Human-readable name
        - description: Brief description of what this tool does
        - install_commands: Array of installation commands (prefer UV if mentioned, otherwise pip)
        - start_command: Command to start/run the tool
        - web_interface: URL if it has a web interface (like http://localhost:PORT)
        - use_venv: true if it needs a virtual environment
        - python_version: Python version requirement (like ">=3.8")
        - requirements_file: Name of requirements file if different from requirements.txt
        
        Focus on finding the actual installation steps from README.md or setup documentation.
        Return ONLY the JSON, no other text.
        """
        
        try:
            response = interpreter.chat(analysis_prompt, display=False)
            
            # Extract JSON from response
            if isinstance(response, list) and len(response) > 0:
                content = response[-1].get('content', '')
                # Try to extract JSON from the response
                json_match = re.search(r'```json\n(.*?)\n```', content, re.DOTALL)
                if json_match:
                    config_data = json.loads(json_match.group(1))
                else:
                    # Try to find JSON directly
                    json_match = re.search(r'\{.*\}', content, re.DOTALL)
                    if json_match:
                        config_data = json.loads(json_match.group(0))
                    else:
                        raise ValueError("No JSON found in response")
                
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
                    requirements_file=config_data.get('requirements_file', 'requirements.txt'),
                    auto_configured=True
                )
                
                print(f"✅ Auto-configured {tool_config.display_name}")
                return tool_config
                
        except Exception as e:
            print(f"⚠️ Auto-configuration failed: {e}")
        
        # Fallback to basic configuration
        return ToolConfig(
            name=name,
            display_name=name.title(),
            source_type=source_type,
            url=url,
            description=f"Tool from {source_type.value}",
            auto_configured=False
        )
    
    def query_project_docs(self, project_name: str, question: str) -> str:
        """Query documentation and code of an installed project"""
        if not INTERPRETER_AVAILABLE:
            return "❌ Open Interpreter not available for doc querying"
        
        # Find the project directory
        project_path = None
        for search_dir in [self.github_dir, self.huggingface_dir, self.custom_dir, self.aiml_home]:
            potential_path = search_dir / project_name
            if potential_path.exists():
                project_path = potential_path
                break
            
            # Also search case-insensitive
            for child in search_dir.iterdir():
                if child.is_dir() and child.name.lower() == project_name.lower():
                    project_path = child
                    break
        
        if not project_path:
            return f"❌ Project '{project_name}' not found in installed tools"
        
        query_prompt = f"""
        You are an AI assistant helping users understand the '{project_name}' project.
        
        Project location: {project_path}
        User question: {question}
        
        Please:
        1. Read the README.md, documentation files, and relevant code files in {project_path}
        2. Answer the user's question based on the project's documentation and code
        3. Provide specific examples, commands, or code snippets when relevant
        4. If the question is about installation, refer to the setup instructions
        5. If the question is about usage, provide practical examples
        
        Be concise but comprehensive in your answer.
        """
        
        try:
            response = interpreter.chat(query_prompt, display=False)
            if isinstance(response, list) and len(response) > 0:
                return response[-1].get('content', 'No response generated')
            return str(response)
        except Exception as e:
            return f"❌ Error querying project docs: {e}"
    
    def _detect_source_type(self, url: str) -> SourceType:
        """Detect the source type from URL"""
        if 'github.com' in url:
            return SourceType.GITHUB
        elif 'huggingface.co' in url:
            return SourceType.HUGGINGFACE
        else:
            return SourceType.CUSTOM
    
    def save_manifest(self, name: str, tools: List[ToolConfig]) -> bool:
        """Save a manifest of tools"""
        try:
            manifest_data = {
                "name": name,
                "created_at": datetime.now().isoformat(),
                "tools": [tool.to_dict() for tool in tools]
            }
            
            manifest_file = self.manifests_dir / f"{name}.json"
            with open(manifest_file, 'w') as f:
                json.dump(manifest_data, f, indent=2)
            
            print(f"💾 Manifest saved: {manifest_file}")
            return True
        except Exception as e:
            print(f"❌ Failed to save manifest: {e}")
            return False
    
    def load_manifest(self, name: str) -> Optional[List[ToolConfig]]:
        """Load a manifest and return list of tools"""
        try:
            manifest_file = self.manifests_dir / f"{name}.json"
            if not manifest_file.exists():
                print(f"❌ Manifest not found: {name}")
                return None
            
            with open(manifest_file, 'r') as f:
                manifest_data = json.load(f)
            
            tools = []
            for tool_dict in manifest_data.get('tools', []):
                tools.append(ToolConfig.from_dict(tool_dict))
            
            return tools
        except Exception as e:
            print(f"❌ Failed to load manifest: {e}")
            return None
    
    def list_manifests(self) -> List[Dict]:
        """List all available manifests"""
        manifests = []
        for manifest_file in self.manifests_dir.glob("*.json"):
            try:
                with open(manifest_file, 'r') as f:
                    data = json.load(f)
                manifests.append({
                    "name": manifest_file.stem,
                    "display_name": data.get("name", manifest_file.stem),
                    "created_at": data.get("created_at", "unknown"),
                    "tool_count": len(data.get("tools", []))
                })
            except Exception as e:
                print(f"⚠️ Error reading manifest {manifest_file}: {e}")
        
        return manifests
    
    def export_manifest(self, name: str, export_path: Path) -> bool:
        """Export a manifest for sharing"""
        try:
            manifest_file = self.manifests_dir / f"{name}.json"
            if not manifest_file.exists():
                print(f"❌ Manifest not found: {name}")
                return False
            
            shutil.copy2(manifest_file, export_path)
            print(f"📤 Manifest exported to: {export_path}")
            return True
        except Exception as e:
            print(f"❌ Failed to export manifest: {e}")
            return False
    
    def import_manifest(self, import_path: Path) -> bool:
        """Import a manifest from file"""
        try:
            if not import_path.exists():
                print(f"❌ Import file not found: {import_path}")
                return False
            
            # Validate JSON structure
            with open(import_path, 'r') as f:
                manifest_data = json.load(f)
            
            if "tools" not in manifest_data:
                print("❌ Invalid manifest format: missing 'tools' key")
                return False
            
            # Copy to manifests directory
            dest_file = self.manifests_dir / import_path.name
            shutil.copy2(import_path, dest_file)
            
            print(f"📥 Manifest imported: {dest_file.stem}")
            return True
        except Exception as e:
            print(f"❌ Failed to import manifest: {e}")
            return False
    
    def get_installed_tools(self) -> List[Dict]:
        """Get list of all installed tools across all sources"""
        installed_tools = []
        
        for source_dir, source_type in [
            (self.github_dir, "github"),
            (self.huggingface_dir, "huggingface"),
            (self.custom_dir, "custom")
        ]:
            for tool_dir in source_dir.iterdir():
                if tool_dir.is_dir():
                    # Try to find metadata
                    metadata_file = tool_dir / ".ams_metadata.json"
                    if metadata_file.exists():
                        try:
                            with open(metadata_file, 'r') as f:
                                metadata = json.load(f)
                            installed_tools.append({
                                "name": tool_dir.name,
                                "source_type": source_type,
                                "path": str(tool_dir),
                                "metadata": metadata
                            })
                        except:
                            pass
                    else:
                        # Basic info without metadata
                        installed_tools.append({
                            "name": tool_dir.name,
                            "source_type": source_type,
                            "path": str(tool_dir),
                            "metadata": {}
                        })
        
        return installed_tools
    
    def create_tool_manifest_from_installed(self) -> ToolConfig:
        """Create a manifest from currently installed tools"""
        installed_tools = self.get_installed_tools()
        
        tools = []
        for tool_info in installed_tools:
            metadata = tool_info.get("metadata", {})
            tool_config = ToolConfig(
                name=tool_info["name"],
                display_name=metadata.get("display_name", tool_info["name"]),
                source_type=SourceType(tool_info["source_type"]),
                url=metadata.get("url", ""),
                description=metadata.get("description", ""),
                install_commands=metadata.get("install_commands", []),
                start_command=metadata.get("start_command", ""),
                web_interface=metadata.get("web_interface", ""),
                use_venv=metadata.get("use_venv", True),
                python_version=metadata.get("python_version", ">=3.8"),
                requirements_file=metadata.get("requirements_file", "requirements.txt")
            )
            tools.append(tool_config)
        
        return tools
    
    def get_source_directory(self, source_type: SourceType) -> Path:
        """Get the directory for a specific source type"""
        if source_type == SourceType.GITHUB:
            return self.github_dir
        elif source_type == SourceType.HUGGINGFACE:
            return self.huggingface_dir
        elif source_type == SourceType.CUSTOM:
            return self.custom_dir
        else:
            return self.custom_dir  # Default fallback
    
    def save_tool_metadata(self, tool_config: ToolConfig, install_path: Path):
        """Save tool metadata for tracking"""
        metadata = {
            "installed_at": datetime.now().isoformat(),
            "display_name": tool_config.display_name,
            "url": tool_config.url,
            "description": tool_config.description,
            "install_commands": tool_config.install_commands,
            "start_command": tool_config.start_command,
            "web_interface": tool_config.web_interface,
            "use_venv": tool_config.use_venv,
            "python_version": tool_config.python_version,
            "requirements_file": tool_config.requirements_file,
            "auto_configured": tool_config.auto_configured
        }
        
        metadata_file = install_path / ".ams_metadata.json"
        try:
            with open(metadata_file, 'w') as f:
                json.dump(metadata, f, indent=2)
        except Exception as e:
            print(f"⚠️ Failed to save metadata: {e}")
