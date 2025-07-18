#!/usr/bin/env python3
"""
🧙‍♂️ Documentation Manager - Intelligent Documentation Analysis

This module provides:
- README and documentation parsing from installed tools
- Knowledge base creation for quick querying
- Natural language Q&A about tool usage
- Code analysis and usage examples extraction
"""

import json
import os
import re
from pathlib import Path
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, asdict

try:
    from interpreter import interpreter
    INTERPRETER_AVAILABLE = True
except ImportError:
    INTERPRETER_AVAILABLE = False


@dataclass
class DocumentationEntry:
    """Represents parsed documentation for a tool"""
    tool_name: str
    tool_path: Path
    readme_content: str = ""
    docs_files: List[str] = None
    code_examples: List[str] = None
    usage_instructions: str = ""
    api_reference: str = ""
    configuration_options: List[str] = None
    last_updated: str = ""
    
    def __post_init__(self):
        if self.docs_files is None:
            self.docs_files = []
        if self.code_examples is None:
            self.code_examples = []
        if self.configuration_options is None:
            self.configuration_options = []


class DocumentationManager:
    """🧙‍♂️ Intelligent Documentation Analysis and Querying System"""
    
    def __init__(self, aiml_home: Path):
        self.aiml_home = Path(aiml_home)
        self.docs_cache_dir = self.aiml_home / "docs_cache"
        self.docs_cache_dir.mkdir(exist_ok=True)
        
        # Knowledge base file
        self.knowledge_base_file = self.docs_cache_dir / "knowledge_base.json"
        self.knowledge_base = self.load_knowledge_base()
        
        if INTERPRETER_AVAILABLE:
            self.setup_interpreter()
    
    def setup_interpreter(self):
        """Configure Open Interpreter for documentation analysis"""
        interpreter.custom_instructions = """
        You are Merlin's Documentation Assistant 📚🧙‍♂️, specialized in analyzing AI/ML tool documentation.
        
        Your expertise includes:
        - Parsing README files and documentation
        - Extracting installation instructions and usage examples
        - Identifying configuration options and API references
        - Answering questions about tool capabilities and usage
        
        Always provide accurate, helpful information based on the actual documentation content.
        """
    
    def scan_installed_tools(self) -> Dict[str, DocumentationEntry]:
        """Scan all installed tools and extract their documentation"""
        print("📚 Scanning installed tools for documentation...")
        
        documentation = {}
        
        # Scan all directories in aiml_home
        for item in self.aiml_home.iterdir():
            if item.is_dir() and item.name not in ['docs_cache', 'manifests']:
                # Check if it's a tool directory or category directory
                if item.name in ['github', 'huggingface', 'custom']:
                    # Scan subdirectories in category folders
                    for tool_dir in item.iterdir():
                        if tool_dir.is_dir():
                            doc_entry = self.analyze_tool_documentation(tool_dir)
                            if doc_entry:
                                documentation[doc_entry.tool_name] = doc_entry
                else:
                    # Direct tool directory
                    doc_entry = self.analyze_tool_documentation(item)
                    if doc_entry:
                        documentation[doc_entry.tool_name] = doc_entry
        
        # Update knowledge base
        self.knowledge_base.update({name: asdict(entry) for name, entry in documentation.items()})
        self.save_knowledge_base()
        
        print(f"📚 Analyzed documentation for {len(documentation)} tools")
        return documentation
    
    def analyze_tool_documentation(self, tool_path: Path) -> Optional[DocumentationEntry]:
        """Analyze documentation for a specific tool"""
        if not tool_path.exists() or not tool_path.is_dir():
            return None
        
        print(f"  📖 Analyzing {tool_path.name}...")
        
        # Find README files
        readme_files = self.find_readme_files(tool_path)
        readme_content = ""
        
        if readme_files:
            # Read the main README
            try:
                with open(readme_files[0], 'r', encoding='utf-8', errors='ignore') as f:
                    readme_content = f.read()
            except Exception as e:
                print(f"    ⚠️ Could not read README: {e}")
        
        # Find documentation files
        docs_files = self.find_documentation_files(tool_path)
        
        # Find code examples
        code_examples = self.find_code_examples(tool_path)
        
        # Extract usage instructions using Open Interpreter if available
        usage_instructions = ""
        configuration_options = []
        
        if INTERPRETER_AVAILABLE and readme_content:
            try:
                usage_instructions, configuration_options = self.extract_usage_info(readme_content, tool_path.name)
            except Exception as e:
                print(f"    ⚠️ Could not extract usage info: {e}")
        
        return DocumentationEntry(
            tool_name=tool_path.name,
            tool_path=tool_path,
            readme_content=readme_content,
            docs_files=[str(f) for f in docs_files],
            code_examples=code_examples,
            usage_instructions=usage_instructions,
            configuration_options=configuration_options,
            last_updated=str(tool_path.stat().st_mtime)
        )
    
    def find_readme_files(self, tool_path: Path) -> List[Path]:
        """Find README files in the tool directory"""
        readme_patterns = ['README.md', 'README.txt', 'README.rst', 'readme.md', 'Readme.md']
        readme_files = []
        
        for pattern in readme_patterns:
            readme_file = tool_path / pattern
            if readme_file.exists():
                readme_files.append(readme_file)
        
        return readme_files
    
    def find_documentation_files(self, tool_path: Path) -> List[Path]:
        """Find documentation files in the tool directory"""
        docs_files = []
        
        # Common documentation directories
        docs_dirs = ['docs', 'documentation', 'doc']
        for docs_dir in docs_dirs:
            docs_path = tool_path / docs_dir
            if docs_path.exists() and docs_path.is_dir():
                for file in docs_path.rglob('*.md'):
                    docs_files.append(file)
                for file in docs_path.rglob('*.rst'):
                    docs_files.append(file)
                for file in docs_path.rglob('*.txt'):
                    docs_files.append(file)
        
        # Also check for common doc files in root
        doc_patterns = ['USAGE.md', 'INSTALL.md', 'TUTORIAL.md', 'GUIDE.md', 'API.md']
        for pattern in doc_patterns:
            doc_file = tool_path / pattern
            if doc_file.exists():
                docs_files.append(doc_file)
        
        return docs_files[:10]  # Limit to prevent overwhelm
    
    def find_code_examples(self, tool_path: Path) -> List[str]:
        """Find code examples in the tool directory"""
        examples = []
        
        # Common example directories
        example_dirs = ['examples', 'example', 'samples', 'demo', 'demos', 'scripts']
        
        for example_dir in example_dirs:
            example_path = tool_path / example_dir
            if example_path.exists() and example_path.is_dir():
                for file in example_path.glob('*.py'):
                    try:
                        with open(file, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                            if len(content) < 5000:  # Only include reasonably sized examples
                                examples.append(f"# {file.name}\n{content}")
                    except Exception:
                        continue
                    
                    if len(examples) >= 5:  # Limit number of examples
                        break
        
        return examples
    
    def extract_usage_info(self, readme_content: str, tool_name: str) -> tuple[str, List[str]]:
        """Extract usage instructions and configuration options using Open Interpreter"""
        if not INTERPRETER_AVAILABLE:
            return "", []
        
        analysis_prompt = f"""
        Analyze this README content for {tool_name} and extract:
        
        1. Key usage instructions (how to run/use the tool)
        2. Configuration options and settings
        
        README Content:
        {readme_content[:8000]}  # Limit content size
        
        Return as JSON with these keys:
        - usage_instructions: string with clear steps to use the tool
        - configuration_options: array of configuration options/settings
        
        Focus on practical usage information.
        """
        
        try:
            response = interpreter.chat(analysis_prompt, display=False)
            
            if isinstance(response, list) and len(response) > 0:
                content = response[-1].get('content', '')
                
                # Try to extract JSON
                import re
                json_match = re.search(r'```json\n(.*?)\n```', content, re.DOTALL)
                if json_match:
                    data = json.loads(json_match.group(1))
                    return (
                        data.get('usage_instructions', ''),
                        data.get('configuration_options', [])
                    )
        except Exception as e:
            print(f"    ⚠️ Failed to extract usage info: {e}")
        
        return "", []
    
    def query_tool_documentation(self, tool_name: str, question: str) -> str:
        """Query documentation for a specific tool using natural language"""
        if not INTERPRETER_AVAILABLE:
            return "❌ Open Interpreter not available for documentation queries"
        
        # Get tool documentation
        if tool_name not in self.knowledge_base:
            # Try to refresh knowledge base
            self.scan_installed_tools()
        
        if tool_name not in self.knowledge_base:
            return f"❌ No documentation found for {tool_name}. Is it installed in your AIML projects folder?"
        
        tool_docs = self.knowledge_base[tool_name]
        
        # Prepare context for Open Interpreter
        context = f"""
        Tool: {tool_name}
        README Content: {tool_docs.get('readme_content', '')[:6000]}
        Usage Instructions: {tool_docs.get('usage_instructions', '')}
        Configuration Options: {', '.join(tool_docs.get('configuration_options', []))}
        Available Examples: {len(tool_docs.get('code_examples', []))} code examples found
        """
        
        query_prompt = f"""
        Based on the documentation for {tool_name}, please answer this question:
        
        Question: {question}
        
        Documentation Context:
        {context}
        
        Provide a helpful, accurate answer based on the available documentation.
        If the documentation doesn't contain the answer, say so and suggest where to look for more information.
        """
        
        try:
            response = interpreter.chat(query_prompt, display=False)
            
            if isinstance(response, list) and len(response) > 0:
                return response[-1].get('content', 'No response generated')
            else:
                return 'No response generated'
                
        except Exception as e:
            return f"❌ Error querying documentation: {e}"
    
    def get_tool_overview(self, tool_name: str) -> Dict[str, Any]:
        """Get a comprehensive overview of a tool's documentation"""
        if tool_name not in self.knowledge_base:
            self.scan_installed_tools()
        
        if tool_name not in self.knowledge_base:
            return {"error": f"No documentation found for {tool_name}"}
        
        tool_docs = self.knowledge_base[tool_name]
        
        overview = {
            "tool_name": tool_name,
            "path": tool_docs.get('tool_path', ''),
            "has_readme": bool(tool_docs.get('readme_content', '')),
            "docs_files_count": len(tool_docs.get('docs_files', [])),
            "code_examples_count": len(tool_docs.get('code_examples', [])),
            "has_usage_instructions": bool(tool_docs.get('usage_instructions', '')),
            "configuration_options_count": len(tool_docs.get('configuration_options', [])),
            "summary": tool_docs.get('readme_content', '')[:500] + "..." if tool_docs.get('readme_content') else "No README found"
        }
        
        return overview
    
    def search_all_documentation(self, query: str) -> List[Dict[str, Any]]:
        """Search across all tool documentation"""
        results = []
        
        for tool_name, tool_docs in self.knowledge_base.items():
            # Simple text search across README and usage instructions
            readme_content = tool_docs.get('readme_content', '').lower()
            usage_instructions = tool_docs.get('usage_instructions', '').lower()
            query_lower = query.lower()
            
            score = 0
            
            # Count matches in README
            score += readme_content.count(query_lower) * 2
            
            # Count matches in usage instructions
            score += usage_instructions.count(query_lower) * 3
            
            # Check configuration options
            config_options = tool_docs.get('configuration_options', [])
            for option in config_options:
                if query_lower in option.lower():
                    score += 5
            
            if score > 0:
                results.append({
                    "tool_name": tool_name,
                    "score": score,
                    "summary": self.extract_relevant_snippet(readme_content, query_lower)
                })
        
        # Sort by relevance score
        results.sort(key=lambda x: x['score'], reverse=True)
        return results[:10]  # Return top 10 results
    
    def extract_relevant_snippet(self, content: str, query: str, context_chars: int = 200) -> str:
        """Extract a relevant snippet around the query match"""
        index = content.lower().find(query.lower())
        if index == -1:
            return content[:200] + "..."
        
        start = max(0, index - context_chars // 2)
        end = min(len(content), index + len(query) + context_chars // 2)
        
        snippet = content[start:end]
        if start > 0:
            snippet = "..." + snippet
        if end < len(content):
            snippet = snippet + "..."
        
        return snippet
    
    def load_knowledge_base(self) -> Dict[str, Any]:
        """Load the knowledge base from disk"""
        if self.knowledge_base_file.exists():
            try:
                with open(self.knowledge_base_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️ Could not load knowledge base: {e}")
        return {}
    
    def save_knowledge_base(self):
        """Save the knowledge base to disk"""
        try:
            # Convert Path objects to strings for JSON serialization
            serializable_kb = {}
            for tool_name, tool_data in self.knowledge_base.items():
                if isinstance(tool_data, dict):
                    serializable_data = {}
                    for key, value in tool_data.items():
                        if isinstance(value, Path):
                            serializable_data[key] = str(value)
                        else:
                            serializable_data[key] = value
                    serializable_kb[tool_name] = serializable_data
                else:
                    serializable_kb[tool_name] = tool_data
            
            with open(self.knowledge_base_file, 'w', encoding='utf-8') as f:
                json.dump(serializable_kb, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"⚠️ Could not save knowledge base: {e}")
    
    def refresh_documentation(self, tool_name: str = None):
        """Refresh documentation for a specific tool or all tools"""
        if tool_name:
            print(f"🔄 Refreshing documentation for {tool_name}...")
            # Find the tool path
            tool_path = None
            for item in self.aiml_home.iterdir():
                if item.is_dir() and item.name == tool_name:
                    tool_path = item
                    break
                elif item.name in ['github', 'huggingface', 'custom']:
                    for subdir in item.iterdir():
                        if subdir.is_dir() and subdir.name == tool_name:
                            tool_path = subdir
                            break
            
            if tool_path:
                doc_entry = self.analyze_tool_documentation(tool_path)
                if doc_entry:
                    self.knowledge_base[tool_name] = asdict(doc_entry)
                    self.save_knowledge_base()
                    print(f"✅ Refreshed documentation for {tool_name}")
                else:
                    print(f"❌ Could not analyze documentation for {tool_name}")
            else:
                print(f"❌ Tool {tool_name} not found")
        else:
            print("🔄 Refreshing all documentation...")
            self.scan_installed_tools()
