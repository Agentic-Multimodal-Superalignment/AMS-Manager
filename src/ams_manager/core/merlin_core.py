#!/usr/bin/env python3
"""
🧙‍♂️ Merlin Core - The Heart of the AMS Manager

This module contains the core intelligence for Merlin, including:
- Environment detection and analysis
- Intelligent package management
- Integration with Open Interpreter
- Smart installation decisions
"""

import json
import yaml
import os
import subprocess
import importlib.util
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass

try:
    from interpreter import interpreter
    INTERPRETER_AVAILABLE = True
except ImportError:
    INTERPRETER_AVAILABLE = False


@dataclass
class PackageInfo:
    """Information about a detected package"""
    name: str
    installed: bool = False
    path: Optional[str] = None
    version: Optional[str] = None
    install_method: Optional[str] = None
    config_files: List[str] = None
    health_status: str = "unknown"
    
    def __post_init__(self):
        if self.config_files is None:
            self.config_files = []


class MerlinCore:
    """
    🧙‍♂️ The Core Intelligence of Merlin
    
    This class handles:
    - Environment detection and scanning
    - Package management and installation
    - Configuration management
    - Integration with existing tools
    """
    
    def __init__(self, config_path: Optional[str] = None, manifest_path: Optional[str] = None):
        self.config_path = config_path or self._find_config_file()
        self.manifest_path = manifest_path or self._find_manifest_file()
        self.config = self.load_config()
        self.manifest = self.load_manifest()
        self.aiml_home = self.get_aiml_home()
        
        # Setup Open Interpreter if available
        if INTERPRETER_AVAILABLE:
            self.setup_interpreter()
        
    def _find_config_file(self) -> str:
        """Find the config.yaml file"""
        possible_paths = [
            Path(__file__).parent.parent / "config" / "config.yaml",
            Path.cwd() / "config.yaml",
            Path.cwd() / "src" / "ams_manager" / "config" / "config.yaml"
        ]
        
        for path in possible_paths:
            if path.exists():
                return str(path)
        
        # Return default path if none found
        return str(Path(__file__).parent.parent / "config" / "config.yaml")
    
    def _find_manifest_file(self) -> str:
        """Find the ams_manifest.json file"""
        possible_paths = [
            Path(__file__).parent.parent / "config" / "ams_manifest.json",
            Path.cwd() / "ams_manifest.json",
            Path.cwd() / "src" / "ams_manager" / "config" / "ams_manifest.json"
        ]
        
        for path in possible_paths:
            if path.exists():
                return str(path)
        
        # Return default path if none found
        return str(Path(__file__).parent.parent / "config" / "ams_manifest.json")
        
    def get_aiml_home(self) -> Path:
        """Get the AI/ML projects home directory"""
        # Check environment variable first
        home_dir = os.environ.get('AIML_PROJECTS_HOME')
        if home_dir:
            return Path(home_dir)
        
        # Check config file
        config_home = self.config.get('aiml_projects_home')
        if config_home:
            return Path(config_home)
        
        # Default to user home/aiml_projects
        return Path.home() / 'aiml_projects'
        
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file"""
        try:
            with open(self.config_path, 'r') as f:
                config = yaml.safe_load(f) or {}
            return {**self.get_default_config(), **config}
        except (FileNotFoundError, yaml.YAMLError) as e:
            print(f"⚠️ Could not load config from {self.config_path}: {e}")
            return self.get_default_config()
            
    def get_default_config(self) -> Dict[str, Any]:
        """Get default configuration"""
        return {
            'profile': 'default',
            'logging': {
                'enabled': True,
                'log_file': 'ams_install.log',
                'verbose': True
            },
            'defaults': {
                'retry_failed': True,
                'dry_run': False,
                'confirm_shell': False
            },
            'aiml_projects_home': str(Path.home() / 'aiml_projects')
        }
        
    def load_manifest(self) -> Dict[str, Any]:
        """Load the installation manifest"""
        try:
            with open(self.manifest_path, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"⚠️ Could not load manifest from {self.manifest_path}: {e}")
            return {'packages': [], 'profiles': {}}
            
    def setup_interpreter(self):
        """Setup Open Interpreter with Merlin's configuration"""
        if not INTERPRETER_AVAILABLE:
            return
            
        # Configure interpreter for AMS tasks
        interpreter.offline = self.config.get('interpreter', {}).get('offline', False)
        interpreter.auto_run = self.config.get('interpreter', {}).get('auto_run', False)
        
        # Set custom instructions for Merlin
        merlin_instructions = """
        You are Merlin, a wise AI assistant specializing in AI/ML tools and the AMS framework.
        You can help with installations, configurations, debugging, and general AI/ML questions.
        You have access to the user's AIML_PROJECTS_HOME directory and can execute commands.
        When helping with installations, always check if tools are already installed first.
        Be helpful, wise, and use wizard-themed language appropriately.
        """
        
        interpreter.custom_instructions = merlin_instructions
        
    def detect_installations(self) -> Dict[str, PackageInfo]:
        """Detect what packages are currently installed"""
        detected = {}
        
        # Get packages from manifest
        packages = self.manifest.get('packages', [])
        
        for package_data in packages:
            package_info = self.detect_package(package_data)
            detected[package_info.name] = package_info
        
        # Also detect common tools not in manifest
        common_tools = self.detect_common_tools()
        detected.update(common_tools)
        
        return detected
        
    def detect_package(self, package_data: Dict[str, Any]) -> PackageInfo:
        """Detect if a specific package is installed"""
        name = package_data.get('name', 'Unknown')
        package_type = package_data.get('type', 'unknown')
        
        # Check in AIML home directory
        expected_path = self.aiml_home / name
        
        package_info = PackageInfo(name=name)
        
        if expected_path.exists():
            package_info.installed = True
            package_info.path = str(expected_path)
            package_info.install_method = package_type
            package_info.version = self.get_package_version(expected_path, package_type)
            package_info.health_status = self.assess_package_health(expected_path, package_data)
            
            # Find config files
            config_patterns = package_data.get('config_patterns', [])
            for pattern in config_patterns:
                config_files = list(expected_path.glob(pattern))
                package_info.config_files.extend([str(f) for f in config_files])
        
        # Also check if it's a Python package
        detection_patterns = package_data.get('detection_patterns', {})
        python_imports = detection_patterns.get('python_imports', [])
        
        for import_name in python_imports:
            if self.is_python_package_installed(import_name):
                if not package_info.installed:  # Only update if not already found
                    package_info.installed = True
                    package_info.install_method = 'pip'
                    package_info.version = self.get_python_package_version(import_name)
        
        return package_info
        
    def detect_common_tools(self) -> Dict[str, PackageInfo]:
        """Detect common AI/ML tools that might not be in the manifest"""
        common_tools = {
            'python': {'command': 'python --version'},
            'pip': {'command': 'pip --version'},
            'git': {'command': 'git --version'},
            'conda': {'command': 'conda --version'},
            'docker': {'command': 'docker --version'},
            'nvidia-smi': {'command': 'nvidia-smi --version'},
        }
        
        detected = {}
        
        for tool_name, tool_info in common_tools.items():
            package_info = PackageInfo(name=tool_name)
            
            # Try to get version via command
            version = self.get_command_version(tool_info['command'])
            if version:
                package_info.installed = True
                package_info.version = version
                package_info.install_method = 'system'
                package_info.health_status = 'healthy'
            
            detected[tool_name] = package_info
        
        return detected
        
    def get_package_version(self, path: Path, package_type: str) -> Optional[str]:
        """Get version of a package at given path"""
        try:
            if package_type == 'github':
                # Try to get git tag or commit
                result = subprocess.run(
                    ['git', 'describe', '--tags', '--always'],
                    cwd=path,
                    capture_output=True,
                    text=True
                )
                if result.returncode == 0:
                    return result.stdout.strip()
            
            # Look for common version files
            version_files = ['version.txt', 'VERSION', '__version__.py']
            for version_file in version_files:
                version_path = path / version_file
                if version_path.exists():
                    with open(version_path, 'r') as f:
                        return f.read().strip()
            
        except Exception:
            pass
        
        return None
        
    def assess_package_health(self, path: Path, package_data: Dict[str, Any]) -> str:
        """Assess the health of an installed package"""
        # Check if main files exist
        main_files = package_data.get('main_files', [])
        for main_file in main_files:
            if not (path / main_file).exists():
                return 'unhealthy'
        
        # Check if it's a git repo and up to date
        if (path / '.git').exists():
            try:
                # Check if there are uncommitted changes
                result = subprocess.run(
                    ['git', 'status', '--porcelain'],
                    cwd=path,
                    capture_output=True,
                    text=True
                )
                if result.stdout.strip():
                    return 'modified'
                
                # Check if behind remote
                subprocess.run(['git', 'fetch'], cwd=path, capture_output=True)
                result = subprocess.run(
                    ['git', 'status', '-uno'],
                    cwd=path,
                    capture_output=True,
                    text=True
                )
                if 'behind' in result.stdout:
                    return 'outdated'
            except Exception:
                pass
        
        return 'healthy'
        
    def is_python_package_installed(self, package_name: str) -> bool:
        """Check if a Python package is installed"""
        try:
            importlib.import_module(package_name)
            return True
        except ImportError:
            return False
                
    def get_python_package_version(self, package_name: str) -> Optional[str]:
        """Get version of an installed Python package"""
        try:
            module = importlib.import_module(package_name)
            # Try common version attributes
            for attr in ['__version__', 'VERSION', 'version']:
                if hasattr(module, attr):
                    return getattr(module, attr)
        except ImportError:
            pass
        
        return None
        
    def get_command_version(self, command: str) -> Optional[str]:
        """Get version by running a command"""
        try:
            result = subprocess.run(
                command.split(),
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                return result.stdout.strip().split('\n')[0]
        except Exception:
            pass
        
        return None
    
    def find_missing_packages(self) -> List[str]:
        """Find packages that are in the manifest but not installed"""
        detected = self.detect_installations()
        profile_packages = self.get_profile_packages()
        
        missing = []
        for package_name in profile_packages:
            if package_name in detected:
                if not detected[package_name].installed:
                    missing.append(package_name)
            else:
                missing.append(package_name)
        
        return missing
    
    def get_profile_packages(self) -> List[str]:
        """Get packages for the current profile"""
        profile_name = self.config.get('profile', 'default')
        profiles = self.manifest.get('profiles', {})
        return profiles.get(profile_name, [])
    
    def install_from_manifest(self, manifest_path: Optional[str] = None):
        """Install packages from manifest"""
        if manifest_path:
            self.manifest_path = manifest_path
            self.manifest = self.load_manifest()
        
        # Use the existing AMS installer for now
        from ams_manager.core.ams_installer import AMSInstaller
        installer = AMSInstaller(self.manifest_path, self.config_path)
        installer.install_all()
    
    def install_packages(self, package_names: List[str]):
        """Install specific packages"""
        packages = self.manifest.get('packages', [])
        packages_to_install = [
            pkg for pkg in packages 
            if pkg.get('name') in package_names
        ]
        
        from ams_manager.core.ams_installer import AMSInstaller
        installer = AMSInstaller(self.manifest_path, self.config_path)
        
        for package in packages_to_install:
            installer.install_package(package)
    
    def get_installation_status(self) -> Dict[str, Dict[str, Any]]:
        """Get current installation status"""
        detected = self.detect_installations()
        
        status = {}
        for name, info in detected.items():
            status[name] = {
                'status': '✅ Installed' if info.installed else '❌ Missing',
                'location': info.path or 'N/A',
                'version': info.version or 'Unknown',
                'health': info.health_status,
                'notes': f"via {info.install_method}" if info.install_method else ""
            }
        
        return status
    
    def chat_with_interpreter(self, message: str) -> Any:
        """Chat with Open Interpreter with Merlin context"""
        if not INTERPRETER_AVAILABLE:
            raise RuntimeError("Open Interpreter not available")
        
        # Add context about current environment
        context = f"""
        Current AIML_PROJECTS_HOME: {self.aiml_home}
        Current profile: {self.config.get('profile', 'default')}
        Available packages in manifest: {[pkg.get('name') for pkg in self.manifest.get('packages', [])]}
        
        User message: {message}
        """
        
        return interpreter.chat(context)
    
    def save_config(self):
        """Save current configuration to file"""
        try:
            with open(self.config_path, 'w') as f:
                yaml.dump(self.config, f, default_flow_style=False)
            return True
        except Exception as e:
            print(f"⚠️ Could not save config: {e}")
            return False
