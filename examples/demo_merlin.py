#!/usr/bin/env python3
"""
🧙‍♂️ Merlin Demo Script

This script demonstrates Merlin's capabilities without requiring full installation.
Perfect for testing and showcasing the system.
"""

import os
import sys
from pathlib import Path
from typing import Dict, Any

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / 'src'))

# Mock classes for demonstration when imports fail
class MockMerlinCore:
    def __init__(self):
        self.aiml_home = Path.home() / 'aiml_projects'
        self.config = {'profile': 'default'}
        
    def detect_installations(self):
        return {
            'ComfyUI': type('', (), {
                'installed': False, 'path': None, 'version': None, 
                'health_status': 'not_installed'
            })(),
            'open-webui': type('', (), {
                'installed': False, 'path': None, 'version': None,
                'health_status': 'not_installed'
            })(),
            'python': type('', (), {
                'installed': True, 'path': sys.executable, 'version': sys.version.split()[0],
                'health_status': 'healthy'
            })()
        }
    
    def find_missing_packages(self):
        return ['ComfyUI', 'open-webui']

class MockEnvironmentDetector:
    def get_system_info(self):
        return type('', (), {
            'system': 'Windows' if os.name == 'nt' else 'Linux',
            'python_version': sys.version.split()[0],
            'python_path': sys.executable,
            'pip_version': 'Unknown',
            'git_available': True,
            'gpu_info': None,
            'total_memory': '16.0 GB',
            'free_space': '50 GB available'
        })()
    
    def scan_for_ai_tools(self):
        return {
            'ComfyUI': {'found': False, 'locations': [], 'details': {}},
            'automatic1111': {'found': False, 'locations': [], 'details': {}},
            'jupyter': {'found': True, 'locations': ['system'], 'details': {'python_packages': ['jupyter']}}
        }


def print_header(title: str):
    """Print a formatted header"""
    print(f"\n{'='*60}")
    print(f"🧙‍♂️ {title}")
    print(f"{'='*60}")


def demo_environment_detection():
    """Demonstrate environment detection capabilities"""
    print_header("Environment Detection Demo")
    
    try:
        from ams_manager.utils.environment_detector import EnvironmentDetector
        detector = EnvironmentDetector()
    except ImportError:
        print("📝 Using mock detector (install dependencies for full functionality)")
        detector = MockEnvironmentDetector()
    
    # Get system info
    print("\n🖥️  System Information:")
    system_info = detector.get_system_info()
    print(f"   Operating System: {system_info.system}")
    print(f"   Python Version: {system_info.python_version}")
    print(f"   Python Path: {system_info.python_path}")
    print(f"   Git Available: {'✅' if system_info.git_available else '❌'}")
    print(f"   Total Memory: {system_info.total_memory}")
    print(f"   Free Space: {system_info.free_space}")
    
    if hasattr(system_info, 'gpu_info') and system_info.gpu_info:
        print(f"   GPU: {system_info.gpu_info}")
    else:
        print("   GPU: Not detected")
    
    # Scan for AI tools
    print("\n🔍 AI/ML Tool Scan:")
    detected_tools = detector.scan_for_ai_tools()
    
    for tool_name, info in detected_tools.items():
        status = "✅ Found" if info.get('found', False) else "❌ Not Found"
        print(f"   {status} {tool_name}")
        
        if info.get('found') and info.get('locations'):
            print(f"      Location: {info['locations'][0]}")


def demo_package_detection():
    """Demonstrate package detection and management"""
    print_header("Package Detection Demo")
    
    try:
        from ams_manager.core.merlin_core import MerlinCore
        merlin = MerlinCore()
    except ImportError:
        print("📝 Using mock core (install dependencies for full functionality)")
        merlin = MockMerlinCore()
    
    print(f"\n📂 AIML Projects Home: {merlin.aiml_home}")
    print(f"🎯 Active Profile: {merlin.config.get('profile', 'default')}")
    
    # Detect installations
    print("\n📦 Package Detection Results:")
    detected = merlin.detect_installations()
    
    for name, info in detected.items():
        if info.installed:
            print(f"   ✅ {name} - Installed")
            if info.path:
                print(f"      Path: {info.path}")
            if info.version:
                print(f"      Version: {info.version}")
            print(f"      Health: {info.health_status}")
        else:
            print(f"   ❌ {name} - Not Installed")
    
    # Show missing packages
    missing = merlin.find_missing_packages()
    if missing:
        print(f"\n📋 Missing Packages: {', '.join(missing)}")
        print("💡 Use 'smart-install' to install only what's missing")
    else:
        print("\n✨ All packages from your profile are installed!")


def demo_cli_interface():
    """Demonstrate CLI interface capabilities"""
    print_header("CLI Interface Demo")
    
    print("🎨 Rich Terminal Interface Features:")
    print("   ✅ Colorful output with emojis")
    print("   ✅ Interactive wizard modes")
    print("   ✅ Progress indicators")
    print("   ✅ Formatted tables and panels")
    print("   ✅ Context-aware help system")
    
    print("\n🧙‍♂️ Available Commands:")
    commands = [
        ("detect", "Scan for AI/ML tools in your environment"),
        ("install", "Install packages from manifest"),
        ("smart-install", "Install only missing packages"),
        ("chat", "Natural language interface with Open Interpreter"),
        ("config", "Configure AIML environment settings"),
        ("status", "Show current installation status")
    ]
    
    for cmd, desc in commands:
        print(f"   📝 {cmd:<15} - {desc}")
    
    print("\n💬 Example Natural Language Commands:")
    examples = [
        "What AI tools do I have installed?",
        "Install ComfyUI for me",
        "Set up my AI projects in ~/my_ai_projects",
        "Show me my environment report",
        "Update all my AI tools"
    ]
    
    for example in examples:
        print(f"   🤖 '{example}'")


def demo_open_interpreter_integration():
    """Demonstrate Open Interpreter integration"""
    print_header("Open Interpreter Integration Demo")
    
    print("🤖 Merlin + Open Interpreter Capabilities:")
    
    features = [
        ("Natural Language Control", "Ask questions in plain English"),
        ("Computer API Access", "GUI automation and screenshot analysis"),
        ("Code Execution", "Safe execution with user confirmation"),
        ("Function Calling", "Direct access to Merlin's functions"),
        ("Streaming Output", "Real-time feedback during operations"),
        ("Custom Instructions", "AI assistant with AI/ML expertise")
    ]
    
    for feature, description in features:
        print(f"   ✨ {feature:<25} - {description}")
    
    # Check if Open Interpreter is available
    try:
        import interpreter
        print("\n✅ Open Interpreter is available!")
        print("🚀 You can use natural language commands with Merlin")
    except ImportError:
        print("\n📦 Open Interpreter not installed")
        print("💡 Install with: pip install open-interpreter")
        print("🚀 Then use: python src/ams_manager/main.py chat")
    
    print("\n🧙‍♂️ Merlin's AI Assistant Features:")
    ai_features = [
        "Intelligent environment analysis",
        "Smart installation recommendations", 
        "Error diagnosis and resolution",
        "Best practice guidance",
        "Workflow automation",
        "Performance optimization tips"
    ]
    
    for feature in ai_features:
        print(f"   🔮 {feature}")


def demo_configuration_management():
    """Demonstrate configuration management"""
    print_header("Configuration Management Demo")
    
    print("⚙️  Configuration Features:")
    
    # Show current environment
    aiml_home = os.environ.get('AIML_PROJECTS_HOME', str(Path.home() / 'aiml_projects'))
    print(f"\n📂 Current AIML_PROJECTS_HOME: {aiml_home}")
    
    # Show configuration structure
    print("\n📁 Configuration Structure:")
    config_items = [
        ("config.yaml", "Main configuration file"),
        ("ams_manifest.json", "Package installation manifest"),
        ("Environment variables", "AIML_PROJECTS_HOME, etc."),
        ("Shell profiles", "Persistent environment setup"),
        ("Installation profiles", "minimal, default, full, development")
    ]
    
    for item, description in config_items:
        print(f"   📄 {item:<20} - {description}")
    
    # Show profile information
    print("\n🎯 Installation Profiles:")
    profiles = {
        'minimal': ['ComfyUI'],
        'default': ['ComfyUI', 'open-webui', 'flux-gym'],
        'full': ['ComfyUI', 'open-webui', 'flux-gym', 'automatic1111', 'invokeai'],
        'development': ['ComfyUI', 'open-webui', 'jupyter-lab']
    }
    
    for profile, packages in profiles.items():
        print(f"   📋 {profile:<12} - {', '.join(packages)}")


def demo_future_roadmap():
    """Show the future roadmap"""
    print_header("Future Roadmap Demo")
    
    print("🚀 What's Coming Next:")
    
    phases = {
        "Phase 1 - Muscle Car (Current)": [
            "✅ Environment detection",
            "✅ Smart installation", 
            "✅ CLI interface",
            "✅ Open Interpreter integration"
        ],
        "Phase 2 - Enhanced Intelligence": [
            "🔄 Computer vision detection",
            "🔄 Auto-configuration",
            "🔄 Update management",
            "🔄 Error recovery"
        ],
        "Phase 3 - Advanced Automation": [
            "🔮 GUI automation",
            "🔮 Model management",
            "🔮 Performance optimization",
            "🔮 Workflow creation"
        ],
        "Phase 4 - Ferrari Version": [
            "✨ Agentic workflows",
            "✨ Multimodal integration",
            "✨ Cloud integration",
            "✨ Enterprise features"
        ]
    }
    
    for phase, features in phases.items():
        print(f"\n📈 {phase}:")
        for feature in features:
            print(f"   {feature}")


def main():
    """Run the complete Merlin demo"""
    print("🧙‍♂️ Welcome to the Merlin AMS Manager Demo!")
    print("This demonstration shows Merlin's current capabilities and future potential.")
    
    # Run all demos
    demo_environment_detection()
    demo_package_detection()
    demo_cli_interface()
    demo_open_interpreter_integration()
    demo_configuration_management()
    demo_future_roadmap()
    
    # Final message
    print_header("Demo Complete")
    print("\n🎉 Thank you for exploring Merlin!")
    print("\n🚀 Ready to get started?")
    print("   1. Run: python setup_merlin.py")
    print("   2. Then: python src/ams_manager/main.py")
    print("\n🧙‍♂️ May your models converge and your installations succeed!")
    print("✨ 'Magic is just science we don't understand yet!' - Merlin")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n🧙‍♂️ Demo interrupted. Thanks for visiting!")
    except Exception as e:
        print(f"\n❌ Demo error: {e}")
        print("This is just a demo - the actual system handles errors more gracefully!")
