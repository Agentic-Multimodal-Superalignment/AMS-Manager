#!/usr/bin/env python3
"""
🧙‍♂️ Merlin AMS Manager Setup Script

This script helps you get started with Merlin quickly by:
- Checking system requirements
- Installing dependencies
- Setting up the environment
- Running initial configuration
"""

import os
import sys
import subprocess
import platform
from pathlib import Path


def print_banner():
    """Print Merlin banner"""
    banner = """
    🧙‍♂️ ✨ MERLIN AMS MANAGER SETUP ✨ 🧙‍♂️
    
    Welcome, apprentice! Let me help you set up your
    magical AI/ML tool management environment.
    
    ════════════════════════════════════════════════
    """
    print(banner)


def check_python_version():
    """Check if Python version is compatible"""
    print("🐍 Checking Python version...")
    
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python {version.major}.{version.minor} detected")
        print("⚠️  Merlin requires Python 3.8 or higher")
        print("   Please upgrade Python and try again")
        return False
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} - Compatible!")
    return True


def check_git():
    """Check if Git is available"""
    print("📦 Checking Git availability...")
    
    try:
        result = subprocess.run(['git', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {result.stdout.strip()}")
            return True
    except FileNotFoundError:
        pass
    
    print("❌ Git not found")
    print("   Git is required for cloning AI/ML repositories")
    
    system = platform.system()
    if system == "Windows":
        print("   Download from: https://git-scm.com/download/windows")
    elif system == "Darwin":
        print("   Install with: brew install git")
        print("   Or download from: https://git-scm.com/download/mac")
    else:
        print("   Install with: sudo apt install git (Ubuntu/Debian)")
        print("   Or: sudo yum install git (CentOS/RHEL)")
    
    return False


def check_disk_space():
    """Check available disk space"""
    print("💾 Checking disk space...")
    
    try:
        if platform.system() == "Windows":
            import shutil
            free_space = shutil.disk_usage("C:\\").free
        else:
            import shutil
            free_space = shutil.disk_usage("/").free
        
        free_gb = free_space / (1024**3)
        
        if free_gb < 10:
            print(f"⚠️  Only {free_gb:.1f} GB free space available")
            print("   Recommend at least 20GB for AI/ML tools")
            return False
        else:
            print(f"✅ {free_gb:.1f} GB free space available")
            return True
            
    except Exception as e:
        print(f"⚠️  Could not check disk space: {e}")
        return True  # Assume it's okay if we can't check


def setup_virtual_environment():
    """Setup virtual environment for Merlin"""
    print("🏗️  Setting up virtual environment...")
    
    venv_path = Path.cwd() / ".venv"
    
    if venv_path.exists():
        print("✅ Virtual environment already exists")
        return True
    
    try:
        # Create virtual environment
        subprocess.run([sys.executable, "-m", "venv", str(venv_path)], check=True)
        print("✅ Virtual environment created")
        
        # Determine activation script
        if platform.system() == "Windows":
            activate_script = venv_path / "Scripts" / "activate"
            pip_exe = venv_path / "Scripts" / "pip"
        else:
            activate_script = venv_path / "bin" / "activate"
            pip_exe = venv_path / "bin" / "pip"
        
        print(f"💡 To activate: source {activate_script}")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to create virtual environment: {e}")
        return False


def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    
    requirements_file = Path("requirements.txt")
    if not requirements_file.exists():
        print("⚠️  requirements.txt not found")
        print("   Creating basic requirements...")
        
        basic_requirements = [
            "pyyaml>=6.0",
            "rich>=13.0.0",
            "click>=8.0.0",
            "requests>=2.28.0",
        ]
        
        try:
            with open(requirements_file, 'w') as f:
                f.write('\n'.join(basic_requirements))
            print("✅ Created basic requirements.txt")
        except Exception as e:
            print(f"❌ Failed to create requirements.txt: {e}")
            return False
    
    try:
        # Install requirements
        subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", str(requirements_file)
        ], check=True)
        print("✅ Dependencies installed successfully")
        
        # Ask about Open Interpreter
        response = input("\n🤖 Install Open Interpreter for AI assistance? (y/n): ").lower()
        if response in ['y', 'yes']:
            print("📦 Installing Open Interpreter...")
            subprocess.run([
                sys.executable, "-m", "pip", "install", "open-interpreter"
            ], check=True)
            print("✅ Open Interpreter installed")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False


def setup_aiml_home():
    """Setup AIML projects home directory"""
    print("📂 Setting up AIML projects directory...")
    
    # Check if already set
    current_home = os.environ.get('AIML_PROJECTS_HOME')
    if current_home:
        print(f"✅ AIML_PROJECTS_HOME already set: {current_home}")
        return Path(current_home)
    
    # Suggest default location
    default_path = Path.home() / "aiml_projects"
    
    print(f"💡 Suggested location: {default_path}")
    response = input("   Use this location? (y/n) or enter custom path: ").strip()
    
    if response.lower() in ['y', 'yes', '']:
        aiml_home = default_path
    elif response.lower() in ['n', 'no']:
        custom_path = input("   Enter custom path: ").strip()
        aiml_home = Path(custom_path)
    else:
        aiml_home = Path(response)
    
    # Create directory
    try:
        aiml_home.mkdir(parents=True, exist_ok=True)
        print(f"✅ Created directory: {aiml_home}")
        
        # Set environment variable for this session
        os.environ['AIML_PROJECTS_HOME'] = str(aiml_home)
        
        # Ask about making it permanent
        response = input("   Make this permanent in your shell profile? (y/n): ").lower()
        if response in ['y', 'yes']:
            add_to_shell_profile('AIML_PROJECTS_HOME', str(aiml_home))
        
        return aiml_home
        
    except Exception as e:
        print(f"❌ Failed to create directory: {e}")
        return None


def add_to_shell_profile(var_name, var_value):
    """Add environment variable to shell profile"""
    export_line = f'export {var_name}="{var_value}"'
    
    # Determine shell profile file
    system = platform.system()
    if system == "Windows":
        print("💡 For Windows, add this to your environment variables:")
        print(f"   Variable: {var_name}")
        print(f"   Value: {var_value}")
        return
    
    profile_files = [
        Path.home() / '.bashrc',
        Path.home() / '.zshrc',
        Path.home() / '.profile'
    ]
    
    for profile_file in profile_files:
        if profile_file.exists():
            try:
                with open(profile_file, 'a') as f:
                    f.write(f'\n# Added by Merlin AMS Manager\n{export_line}\n')
                print(f"✅ Added to {profile_file}")
                print("💡 Run 'source ~/.bashrc' or restart your terminal")
                return
            except Exception as e:
                print(f"⚠️  Could not write to {profile_file}: {e}")
    
    print("⚠️  No shell profile found. Add manually:")
    print(f"   {export_line}")


def run_initial_setup():
    """Run initial Merlin setup"""
    print("⚙️  Running initial Merlin setup...")
    
    try:
        # Import and initialize Merlin
        sys.path.insert(0, str(Path("src")))
        from ams_manager.core.merlin_core import MerlinCore
        
        merlin = MerlinCore()
        print(f"✅ Merlin initialized successfully")
        print(f"   AIML Home: {merlin.aiml_home}")
        print(f"   Config: {merlin.config_path}")
        print(f"   Manifest: {merlin.manifest_path}")
        
        return True
        
    except Exception as e:
        print(f"⚠️  Could not initialize Merlin: {e}")
        print("   You can still use Merlin manually")
        return False


def print_next_steps():
    """Print what to do next"""
    next_steps = """
🎉 Setup Complete! Here's what you can do next:

🚀 Quick Start:
   python src/ams_manager/main.py

🔍 Detect AI/ML tools:
   python src/ams_manager/main.py detect

📦 Install missing packages:
   python src/ams_manager/main.py smart-install

🤖 Chat with Merlin (if Open Interpreter installed):
   python src/ams_manager/main.py chat

📚 Examples:
   python examples/ams_manager_example.py

📖 Full Documentation:
   See README.md and docs/ directory

═══════════════════════════════════════════════════

🧙‍♂️ "Magic is just science we don't understand yet!"
   - Merlin, your AI/ML assistant
"""
    print(next_steps)


def main():
    """Main setup function"""
    print_banner()
    
    # Check system requirements
    checks = [
        ("Python Version", check_python_version),
        ("Git", check_git),
        ("Disk Space", check_disk_space),
    ]
    
    print("🔍 System Requirements Check:")
    print("═" * 30)
    
    failed_checks = []
    for check_name, check_func in checks:
        if not check_func():
            failed_checks.append(check_name)
    
    if failed_checks:
        print(f"\n❌ Failed checks: {', '.join(failed_checks)}")
        print("   Please resolve these issues before continuing")
        sys.exit(1)
    
    print("\n✅ All system checks passed!")
    
    # Setup environment
    print("\n🏗️  Environment Setup:")
    print("═" * 20)
    
    steps = [
        ("Virtual Environment", setup_virtual_environment),
        ("Dependencies", install_dependencies),
        ("AIML Home Directory", setup_aiml_home),
        ("Merlin Initialization", run_initial_setup),
    ]
    
    for step_name, step_func in steps:
        print(f"\n{step_name}:")
        result = step_func()
        if result is False:
            print(f"⚠️  {step_name} setup had issues, but continuing...")
    
    print_next_steps()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n🧙‍♂️ Setup interrupted. You can run this again anytime!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Setup failed with error: {e}")
        print("   Please check the error and try again")
        sys.exit(1)
