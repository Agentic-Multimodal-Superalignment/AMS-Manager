#!/usr/bin/env python3
"""
🧙‍♂️ Merlin AMS Manager Example

This example demonstrates how to use Merlin for AI/ML tool management.
"""

import sys
from pathlib import Path

# Add the src directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from ams_manager.core.merlin_core import MerlinCore
from ams_manager.utils.environment_detector import EnvironmentDetector
from ams_manager.cli.ams_manager_cli import MerlinCLI

def main():
    """Demonstrate Merlin's capabilities"""
    
    print("🧙‍♂️ Welcome to the Merlin AMS Manager Example!")
    print("=" * 50)
    
    # Initialize Merlin Core
    print("\n1. Initializing Merlin Core...")
    merlin = MerlinCore()
    print(f"   ✅ Merlin initialized with AIML home: {merlin.aiml_home}")
    print(f"   📋 Active profile: {merlin.config.get('profile', 'default')}")
    
    # Demonstrate environment detection
    print("\n2. Detecting AI/ML Environment...")
    env_detector = EnvironmentDetector()
    system_info = env_detector.get_system_info()
    
    print(f"   🖥️  System: {system_info.system}")
    print(f"   🐍 Python: {system_info.python_version}")
    print(f"   📦 Pip: {system_info.pip_version}")
    print(f"   📁 Git: {'✅' if system_info.git_available else '❌'}")
    
    if system_info.gpu_info:
        print(f"   🎮 GPU: {list(system_info.gpu_info.keys())}")
    else:
        print("   🎮 GPU: Not detected")
    
    # Detect installations
    print("\n3. Scanning for AI/ML Tools...")
    detected = merlin.detect_installations()
    
    print(f"   📊 Found {len(detected)} tools in manifest:")
    for name, info in detected.items():
        status = "✅ Installed" if info.installed else "❌ Missing"
        version = f" (v{info.version})" if info.version else ""
        print(f"      {status} {name}{version}")
    
    # Show missing packages
    print("\n4. Analyzing Missing Packages...")
    missing = merlin.find_missing_packages()
    if missing:
        print(f"   📋 Missing packages: {', '.join(missing)}")
        print("   💡 Run smart_install() to install them automatically")
    else:
        print("   ✨ All packages from your profile are installed!")
    
    # Demonstrate package information
    print("\n5. Package Information Example...")
    packages = merlin.manifest.get('packages', [])
    if packages:
        example_package = packages[0]['name']
        print(f"   📦 Information for {example_package}:")
        
        # Get package data from manifest
        package_data = packages[0]
        print(f"      Description: {package_data.get('description', 'N/A')}")
        print(f"      Type: {package_data.get('type', 'N/A')}")
        print(f"      URL: {package_data.get('url', 'N/A')}")
        
        # Get detection info
        if example_package in detected:
            info = detected[example_package]
            print(f"      Status: {'✅ Installed' if info.installed else '❌ Missing'}")
            if info.path:
                print(f"      Path: {info.path}")
    
    # Show configuration
    print("\n6. Configuration Overview...")
    print(f"   📂 AIML Projects Home: {merlin.aiml_home}")
    print(f"   ⚙️  Config file: {merlin.config_path}")
    print(f"   📋 Manifest file: {merlin.manifest_path}")
    print(f"   🎯 Current profile: {merlin.config.get('profile', 'default')}")
    
    # Available profiles
    profiles = merlin.manifest.get('profiles', {})
    if profiles:
        print(f"   📑 Available profiles: {', '.join(profiles.keys())}")
    
    print("\n" + "=" * 50)
    print("🧙‍♂️ Example complete! Here's what you can do next:")
    print()
    print("🎯 Interactive Mode:")
    print("   python src/ams_manager/main.py")
    print()
    print("🔍 Detect installations:")
    print("   python src/ams_manager/main.py detect")
    print()
    print("📦 Smart install missing packages:")
    print("   python src/ams_manager/main.py smart-install")
    print()
    print("🤖 Chat with Merlin (requires Open Interpreter):")
    print("   python src/ams_manager/main.py chat")
    print()
    print("💡 For a complete list of commands:")
    print("   python src/ams_manager/main.py --help")
    

def demo_cli():
    """Demonstrate CLI functionality"""
    print("\n🧙‍♂️ CLI Demo Mode")
    print("=" * 30)
    
    # Initialize CLI
    merlin_core = MerlinCore()
    cli = MerlinCLI(merlin_core)
    
    # Demonstrate detection
    print("\n📊 Detection Results:")
    cli.detect_installations()
    
    print("\n📋 Status Overview:")
    cli.show_status()


def demo_environment_report():
    """Generate and display a comprehensive environment report"""
    print("\n🧙‍♂️ Environment Report Demo")
    print("=" * 35)
    
    env_detector = EnvironmentDetector()
    report = env_detector.generate_environment_report()
    
    print(f"📊 Report generated at: {report.get('timestamp', 'Unknown')}")
    
    # System info summary
    system_info = report.get('system_info', {})
    print(f"\n🖥️  System Overview:")
    print(f"   OS: {system_info.get('system', 'Unknown')}")
    print(f"   Python: {system_info.get('python_version', 'Unknown')}")
    print(f"   Memory: {system_info.get('total_memory', 'Unknown')}")
    print(f"   GPU: {system_info.get('gpu_info', 'Not detected')}")
    
    # Tool detection summary
    detected_tools = report.get('detected_tools', {})
    found_tools = [name for name, info in detected_tools.items() if info.get('found', False)]
    print(f"\n🔍 Detected AI/ML Tools ({len(found_tools)} found):")
    for tool in found_tools[:5]:  # Show first 5
        print(f"   ✅ {tool}")
    
    # Python packages summary
    python_packages = report.get('python_packages', {})
    print(f"\n🐍 Key Python Packages ({len(python_packages)} found):")
    for package, version in list(python_packages.items())[:5]:  # Show first 5
        print(f"   📦 {package}: {version}")


if __name__ == "__main__":
    # Run the main example
    main()
    
    # Optionally run other demos
    import sys
    if len(sys.argv) > 1:
        if sys.argv[1] == "cli":
            demo_cli()
        elif sys.argv[1] == "report":
            demo_environment_report()
        else:
            print("\nUsage:")
            print("  python ams_manager_example.py         # Main example")
            print("  python ams_manager_example.py cli     # CLI demo")
            print("  python ams_manager_example.py report  # Environment report demo")
