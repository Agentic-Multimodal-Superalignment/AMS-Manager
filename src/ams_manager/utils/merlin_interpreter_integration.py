#!/usr/bin/env python3
"""
🧙‍♂️ Merlin Integration - Bridge between Open Interpreter and AMS Manager

This module provides seamless integration between Merlin and Open Interpreter,
allowing natural language control of the AMS Manager system.
"""
import os
import sys
import json
from pathlib import Path
from typing import Dict, List, Optional, Any

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from interpreter import interpreter
    INTERPRETER_AVAILABLE = True
except ImportError:
    INTERPRETER_AVAILABLE = False

from core.merlin_core import MerlinCore
from utils.environment_detector import EnvironmentDetector


class MerlinInterpreterBridge:
    """
    🧙‍♂️ Bridge between Merlin and Open Interpreter
    
    This class allows Open Interpreter to seamlessly access Merlin's capabilities
    through natural language commands.
    """
    
    def __init__(self):
        self.merlin_core = MerlinCore()
        self.env_detector = EnvironmentDetector()
        
        if INTERPRETER_AVAILABLE:
            self.setup_interpreter_context()
        
    def setup_interpreter_context(self):
        """Setup Open Interpreter with Merlin's context and capabilities"""
        if not INTERPRETER_AVAILABLE:
            return
        
        # Configure interpreter settings
        interpreter.offline = False  # Allow online capabilities
        interpreter.auto_run = False  # Always ask for confirmation for safety
        interpreter.custom_instructions = self.get_merlin_system_message()
        
        # Register Merlin's functions with interpreter
        self.register_merlin_functions()
        
    def get_merlin_system_message(self) -> str:
        """Get Merlin's system message for Open Interpreter"""
        current_env = self.merlin_core.get_aiml_home()
        profile = self.merlin_core.config.get('profile', 'default')
        
        return f"""
You are Merlin 🧙‍♂️, a wise and helpful AI assistant specializing in AI/ML tools and the AMS (Agentic Multimodal Superalignment) framework.

## Your Capabilities:
- **Environment Detection**: Scan and analyze AI/ML installations
- **Smart Installation**: Install only missing packages intelligently  
- **Configuration Management**: Handle AI/ML project directories and settings
- **Package Management**: Work with ComfyUI, Open WebUI, Flux Gym, and other tools
- **System Integration**: Use computer APIs for advanced tasks

## Current Environment:
- AIML_PROJECTS_HOME: {current_env}
- Active Profile: {profile}
- System: {sys.platform}

## Available Functions:
You have access to these Merlin functions (use them when appropriate):
- detect_installations() - Scan for AI/ML tools
- install_package(name) - Install specific package
- smart_install() - Install only missing packages
- get_environment_report() - Comprehensive environment analysis
- configure_aiml_home(path) - Set AI/ML projects directory
- show_package_info(name) - Get details about a package
- get_status() - Show installation status

## Personality:
- Be helpful, wise, and knowledgeable about AI/ML
- Use wizard-themed language appropriately (🧙‍♂️, ✨, 🔮)
- Always prioritize user safety and ask before executing commands
- Explain what you're doing and why
- Be concise but thorough in explanations

## Guidelines:
- Always check what's already installed before suggesting installations
- Prefer the AIML_PROJECTS_HOME directory for new installations
- Use proper error handling and provide helpful error messages
- When in doubt, ask the user for clarification
- Suggest best practices for AI/ML development workflows

Remember: You have the power of Open Interpreter to execute code and automate tasks, but use this power wisely! 🧙‍♂️✨
"""

    def register_merlin_functions(self):
        """Register Merlin's functions with Open Interpreter context"""
        # This creates a context where interpreter can call these functions
        merlin_functions = {
            'detect_installations': self.detect_installations,
            'install_package': self.install_package,
            'smart_install': self.smart_install,
            'get_environment_report': self.get_environment_report,
            'configure_aiml_home': self.configure_aiml_home,
            'show_package_info': self.show_package_info,
            'get_status': self.get_status,
            'show_help': self.show_help
        }
        
        # Note: In a real implementation, you might use interpreter's function calling capabilities
        # For now, we'll make these available in the global namespace when needed
        
    def detect_installations(self) -> Dict[str, Any]:
        """Detect current AI/ML installations"""
        try:
            print("🔍 Merlin is scanning your environment for AI/ML tools...")
            
            # Use both core detection and environment detector
            core_detected = self.merlin_core.detect_installations()
            env_detected = self.env_detector.scan_for_ai_tools()
            
            # Combine results
            combined_results = {
                'core_detected': {name: {
                    'installed': info.installed,
                    'path': info.path,
                    'version': info.version,
                    'health': info.health_status
                } for name, info in core_detected.items()},
                'environment_scan': env_detected,
                'summary': {
                    'total_tools_checked': len(core_detected) + len(env_detected),
                    'installed_count': sum(1 for info in core_detected.values() if info.installed),
                    'aiml_home': str(self.merlin_core.aiml_home)
                }
            }
            
            print(f"✅ Scan complete! Found {combined_results['summary']['installed_count']} installed tools.")
            return combined_results
            
        except Exception as e:
            error_msg = f"⚠️ Detection failed: {str(e)}"
            print(error_msg)
            return {'error': error_msg}
    
    def install_package(self, package_name: str) -> Dict[str, Any]:
        """Install a specific package"""
        try:
            print(f"📦 Merlin is preparing to install {package_name}...")
            
            # Check if already installed
            detected = self.merlin_core.detect_installations()
            if package_name in detected and detected[package_name].installed:
                return {
                    'status': 'already_installed',
                    'message': f"✅ {package_name} is already installed at {detected[package_name].path}",
                    'details': {
                        'path': detected[package_name].path,
                        'version': detected[package_name].version
                    }
                }
            
            # Proceed with installation
            self.merlin_core.install_packages([package_name])
            
            return {
                'status': 'success',
                'message': f"✅ {package_name} installation completed!",
                'next_steps': f"Check {self.merlin_core.aiml_home} for the installed package."
            }
            
        except Exception as e:
            error_msg = f"⚠️ Installation failed: {str(e)}"
            print(error_msg)
            return {'status': 'error', 'error': error_msg}
    
    def smart_install(self) -> Dict[str, Any]:
        """Intelligently install only missing packages"""
        try:
            print("🎯 Merlin is analyzing what you need and installing only missing packages...")
            
            missing_packages = self.merlin_core.find_missing_packages()
            
            if not missing_packages:
                return {
                    'status': 'complete',
                    'message': "✨ Everything is already installed! Your environment is complete.",
                    'missing_count': 0
                }
            
            print(f"📋 Found {len(missing_packages)} missing packages: {', '.join(missing_packages)}")
            
            # Install missing packages
            self.merlin_core.install_packages(missing_packages)
            
            return {
                'status': 'success',
                'message': f"✅ Smart installation complete! Installed {len(missing_packages)} packages.",
                'installed_packages': missing_packages,
                'location': str(self.merlin_core.aiml_home)
            }
            
        except Exception as e:
            error_msg = f"⚠️ Smart installation failed: {str(e)}"
            print(error_msg)
            return {'status': 'error', 'error': error_msg}
    
    def get_environment_report(self) -> Dict[str, Any]:
        """Get comprehensive environment report"""
        try:
            print("📊 Merlin is generating your comprehensive environment report...")
            
            # Get system info
            system_info = self.env_detector.get_system_info()
            
            # Get installation status
            installations = self.merlin_core.get_installation_status()
            
            # Get Python packages
            python_packages = self.env_detector.scan_python_packages()
            
            # Get tool detection
            detected_tools = self.env_detector.scan_for_ai_tools()
            
            report = {
                'timestamp': str(system_info),
                'system': {
                    'os': system_info.system,
                    'python_version': system_info.python_version,
                    'python_path': system_info.python_path,
                    'virtual_env': system_info.virtual_env,
                    'conda_env': system_info.conda_env,
                    'gpu_info': system_info.gpu_info,
                    'memory': system_info.total_memory,
                    'disk_space': system_info.free_space
                },
                'aiml_environment': {
                    'home_directory': str(self.merlin_core.aiml_home),
                    'active_profile': self.merlin_core.config.get('profile', 'default'),
                    'config_path': self.merlin_core.config_path
                },
                'installations': installations,
                'detected_tools': detected_tools,
                'python_packages': python_packages,
                'recommendations': self._generate_recommendations(installations, system_info)
            }
            
            print("✅ Environment report generated successfully!")
            return report
            
        except Exception as e:
            error_msg = f"⚠️ Report generation failed: {str(e)}"
            print(error_msg)
            return {'error': error_msg}
    
    def configure_aiml_home(self, path: Optional[str] = None) -> Dict[str, Any]:
        """Configure AIML projects home directory"""
        try:
            if path is None:
                current_path = str(self.merlin_core.aiml_home)
                return {
                    'current_path': current_path,
                    'message': f"Current AIML_PROJECTS_HOME: {current_path}",
                    'instructions': "To change, call configure_aiml_home('/new/path')"
                }
            
            print(f"⚙️ Merlin is configuring AIML_PROJECTS_HOME to {path}...")
            
            # Validate and create path
            new_path = Path(path)
            new_path.mkdir(parents=True, exist_ok=True)
            
            # Update environment variable
            os.environ['AIML_PROJECTS_HOME'] = str(new_path)
            
            # Update config
            self.merlin_core.config['aiml_projects_home'] = str(new_path)
            self.merlin_core.save_config()
            
            # Reinitialize with new path
            self.merlin_core.aiml_home = new_path
            
            return {
                'status': 'success',
                'old_path': str(self.merlin_core.aiml_home),
                'new_path': str(new_path),
                'message': f"✅ AIML_PROJECTS_HOME updated to {new_path}",
                'note': "Restart your shell or run 'source ~/.bashrc' to make permanent"
            }
            
        except Exception as e:
            error_msg = f"⚠️ Configuration failed: {str(e)}"
            print(error_msg)
            return {'status': 'error', 'error': error_msg}
    
    def show_package_info(self, package_name: str) -> Dict[str, Any]:
        """Show detailed information about a package"""
        try:
            print(f"📋 Merlin is gathering information about {package_name}...")
            
            # Get from manifest
            packages = self.merlin_core.manifest.get('packages', [])
            package_data = next((pkg for pkg in packages if pkg.get('name') == package_name), None)
            
            if not package_data:
                return {
                    'status': 'not_found',
                    'message': f"❌ Package '{package_name}' not found in manifest",
                    'available_packages': [pkg.get('name') for pkg in packages]
                }
            
            # Get detection info
            detected = self.merlin_core.detect_installations()
            detection_info = detected.get(package_name, None)
            
            return {
                'status': 'found',
                'package_data': package_data,
                'detection_info': {
                    'installed': detection_info.installed if detection_info else False,
                    'path': detection_info.path if detection_info else None,
                    'version': detection_info.version if detection_info else None,
                    'health': detection_info.health_status if detection_info else 'unknown'
                } if detection_info else None,
                'message': f"📦 Information for {package_name} retrieved successfully"
            }
            
        except Exception as e:
            error_msg = f"⚠️ Failed to get package info: {str(e)}"
            print(error_msg)
            return {'status': 'error', 'error': error_msg}
    
    def get_status(self) -> Dict[str, Any]:
        """Get current installation status"""
        try:
            print("📋 Merlin is checking your current installation status...")
            
            status = self.merlin_core.get_installation_status()
            profile_packages = self.merlin_core.get_profile_packages()
            
            # Count statistics
            total_packages = len(status)
            installed_packages = sum(1 for pkg_status in status.values() if '✅' in pkg_status['status'])
            missing_packages = total_packages - installed_packages
            
            return {
                'status': status,
                'summary': {
                    'total_packages': total_packages,
                    'installed': installed_packages,
                    'missing': missing_packages,
                    'profile': self.merlin_core.config.get('profile', 'default'),
                    'profile_packages': profile_packages,
                    'aiml_home': str(self.merlin_core.aiml_home)
                },
                'message': f"📊 Status: {installed_packages}/{total_packages} packages installed"
            }
            
        except Exception as e:
            error_msg = f"⚠️ Status check failed: {str(e)}"
            print(error_msg)
            return {'status': 'error', 'error': error_msg}
    
    def show_help(self) -> Dict[str, str]:
        """Show help information for Merlin functions"""
        return {
            'detect_installations': 'Scan for AI/ML tools in your environment',
            'install_package(name)': 'Install a specific package by name',
            'smart_install()': 'Install only missing packages from your profile',
            'get_environment_report()': 'Generate comprehensive environment analysis',
            'configure_aiml_home(path)': 'Set or view AIML projects directory',
            'show_package_info(name)': 'Get detailed info about a package',
            'get_status()': 'Show current installation status',
            'example_usage': 'Ask Merlin: "Install ComfyUI for me" or "What AI tools do I have installed?"'
        }
    
    def _generate_recommendations(self, installations: Dict[str, Any], system_info) -> List[str]:
        """Generate recommendations based on environment analysis"""
        recommendations = []
        
        # Check for missing core tools
        if 'git' not in installations or not installations['git']['status'].startswith('✅'):
            recommendations.append("Install Git for version control and cloning repositories")
        
        # Check for Python environment
        if not system_info.virtual_env and not system_info.conda_env:
            recommendations.append("Consider using a virtual environment (venv/conda) for better dependency management")
        
        # Check for GPU setup
        if not system_info.gpu_info:
            recommendations.append("No GPU detected - AI/ML tasks will run on CPU (slower)")
        elif 'nvidia' in system_info.gpu_info:
            recommendations.append("NVIDIA GPU detected - ensure CUDA is properly installed for optimal performance")
        
        # Check for missing AI tools
        missing_tools = [name for name, info in installations.items() 
                        if not info['status'].startswith('✅') and name in ['ComfyUI', 'open-webui']]
        if missing_tools:
            recommendations.append(f"Consider installing: {', '.join(missing_tools)}")
        
        # Memory recommendations
        if system_info.total_memory:
            try:
                memory_gb = float(system_info.total_memory.split()[0])
                if memory_gb < 16:
                    recommendations.append("16GB+ RAM recommended for optimal AI/ML performance")
            except:
                pass
        
        return recommendations


def setup_open_interpreter_integration():
    """Setup Open Interpreter with Merlin integration"""
    if not INTERPRETER_AVAILABLE:
        print("⚠️ Open Interpreter not available. Install with: pip install open-interpreter")
        return None
    
    bridge = MerlinInterpreterBridge()
    
    print("🧙‍♂️ Merlin is ready! You can now ask natural language questions about AI/ML tools.")
    print("Examples:")
    print("  - 'What AI tools do I have installed?'")
    print("  - 'Install ComfyUI for me'") 
    print("  - 'Set up my AI projects in ~/my_ai_projects'")
    print("  - 'Show me my environment report'")
    
    return bridge


if __name__ == "__main__":
    # Demo/test the integration
    bridge = setup_open_interpreter_integration()
    
    if bridge and INTERPRETER_AVAILABLE:
        print("\n🧙‍♂️ Starting Merlin chat session...")
        interpreter.chat("Hello Merlin! Please introduce yourself and show me what AI tools I have installed.")
    else:
        print("❌ Cannot start - Open Interpreter not available")
