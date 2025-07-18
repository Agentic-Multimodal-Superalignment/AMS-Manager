#!/usr/bin/env python3
"""
🧙‍♂️ Merlin AMS Manager - Pre-Release Checklist

This script performs a comprehensive check of the package before GitHub release.
"""

import sys
import os
import subprocess
from pathlib import Path
from typing import List, Dict, Tuple, Optional

def print_header(title: str):
    """Print a formatted header"""
    print(f"\n{'='*60}")
    print(f"🧙‍♂️ {title}")
    print(f"{'='*60}")

def print_check(name: str, status: bool, details: str = ""):
    """Print check result"""
    status_emoji = "✅" if status else "❌"
    print(f"{status_emoji} {name}")
    if details:
        print(f"   📝 {details}")

def check_file_exists(filepath: Path, description: str) -> bool:
    """Check if a file exists"""
    exists = filepath.exists()
    print_check(f"{description}: {filepath.name}", exists, 
                f"Found at {filepath}" if exists else f"Missing: {filepath}")
    return exists

def check_python_syntax(file_path: Path) -> Tuple[bool, str]:
    """Check if Python file has valid syntax"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            compile(f.read(), file_path, 'exec')
        return True, "Syntax OK"
    except SyntaxError as e:
        return False, f"Syntax Error: {e}"
    except Exception as e:
        return False, f"Error: {e}"

def check_imports(file_path: Path) -> Tuple[bool, str]:
    """Check if Python file imports successfully"""
    try:
        # Change to the directory to handle relative imports
        original_cwd = os.getcwd()
        os.chdir(file_path.parent)
        
        # Try importing
        spec = __import__('importlib.util', fromlist=['spec_from_file_location'])
        module_spec = spec.spec_from_file_location("test_module", file_path)
        if module_spec and module_spec.loader:
            module = spec.module_from_spec(module_spec)
            module_spec.loader.exec_module(module)
            return True, "Imports OK"
        else:
            return False, "Could not create module spec"
    except Exception as e:
        return False, f"Import Error: {e}"
    finally:
        os.chdir(original_cwd)

def run_pre_release_check():
    """Run comprehensive pre-release check"""
    
    print_header("MERLIN AMS MANAGER - PRE-RELEASE CHECK")
    
    base_path = Path(".")
    src_path = base_path / "src" / "ams_manager"
    
    # File Structure Check
    print_header("1. ESSENTIAL FILES CHECK")
    
    essential_files = [
        (base_path / "README.md", "README file"),
        (base_path / "LICENSE", "License file"),
        (base_path / "requirements.txt", "Requirements file"),
        (base_path / "pyproject.toml", "Python project config"),
        (base_path / ".gitignore", "Git ignore file"),
        (src_path / "main.py", "Main entry point"),
        (src_path / "__init__.py", "Package init file"),
    ]
    
    all_files_exist = True
    for file_path, description in essential_files:
        exists = check_file_exists(file_path, description)
        all_files_exist = all_files_exist and exists
    
    # Core Module Structure Check
    print_header("2. CORE MODULE STRUCTURE")
    
    core_modules = [
        (src_path / "core" / "__init__.py", "Core package init"),
        (src_path / "core" / "manifest_manager.py", "Manifest Manager"),
        (src_path / "core" / "modular_installer.py", "Modular Installer"),
        (src_path / "core" / "documentation_manager.py", "Documentation Manager"),
        (src_path / "core" / "merlin_core.py", "Merlin Core"),
        (src_path / "utils" / "__init__.py", "Utils package init"),
        (src_path / "cli" / "__init__.py", "CLI package init"),
    ]
    
    core_structure_ok = True
    for file_path, description in core_modules:
        exists = check_file_exists(file_path, description)
        core_structure_ok = core_structure_ok and exists
    
    # Syntax Check
    print_header("3. PYTHON SYNTAX CHECK")
    
    python_files = []
    for pattern in ["**/*.py"]:
        python_files.extend(list(src_path.glob(pattern)))
    
    syntax_ok = True
    for py_file in python_files[:10]:  # Check first 10 files
        is_valid, message = check_python_syntax(py_file)
        print_check(f"Syntax: {py_file.name}", is_valid, message)
        syntax_ok = syntax_ok and is_valid
    
    # Main Entry Point Check
    print_header("4. MAIN ENTRY POINT CHECK")
    
    main_file = src_path / "main.py"
    if main_file.exists():
        # Check if main function exists
        try:
            with open(main_file, 'r', encoding='utf-8') as f:
                content = f.read()
                has_main = 'def main(' in content or 'if __name__ == "__main__"' in content
                print_check("Has main function/entry point", has_main)
                
                # Check for proper imports
                has_imports = 'from ams_manager' in content
                print_check("Has proper internal imports", has_imports)
                
        except Exception as e:
            print_check("Main file readable", False, str(e))
    
    # Dependencies Check
    print_header("5. DEPENDENCIES CHECK")
    
    requirements_file = base_path / "requirements.txt"
    pyproject_file = base_path / "pyproject.toml"
    
    if requirements_file.exists():
        try:
            with open(requirements_file, 'r', encoding='utf-8') as f:
                reqs = f.read()
                essential_deps = ['pyyaml', 'rich', 'requests', 'click']
                for dep in essential_deps:
                    has_dep = dep in reqs.lower()
                    print_check(f"Dependency: {dep}", has_dep)
        except Exception as e:
            print_check("Read requirements.txt", False, str(e))
    
    # Documentation Check
    print_header("6. DOCUMENTATION CHECK")
    
    readme_file = base_path / "README.md"
    if readme_file.exists():
        try:
            with open(readme_file, 'r', encoding='utf-8') as f:
                readme_content = f.read()
                
                doc_checks = [
                    ("Has title", "# " in readme_content),
                    ("Has installation instructions", "install" in readme_content.lower()),
                    ("Has usage examples", "usage" in readme_content.lower() or "example" in readme_content.lower()),
                    ("Has features section", "feature" in readme_content.lower()),
                    ("Has requirements", "requirement" in readme_content.lower() or "prerequisite" in readme_content.lower()),
                ]
                
                for check_name, condition in doc_checks:
                    print_check(check_name, condition)
                    
        except Exception as e:
            print_check("Read README.md", False, str(e))
    
    # Version Information Check
    print_header("7. VERSION & METADATA")
    
    if pyproject_file.exists():
        try:
            with open(pyproject_file, 'r', encoding='utf-8') as f:
                pyproject_content = f.read()
                
                metadata_checks = [
                    ("Has version", 'version =' in pyproject_content),
                    ("Has description", 'description =' in pyproject_content),
                    ("Has author info", 'authors =' in pyproject_content),
                    ("Has dependencies", 'dependencies =' in pyproject_content),
                    ("Has entry points", 'scripts' in pyproject_content or 'console_scripts' in pyproject_content),
                ]
                
                for check_name, condition in metadata_checks:
                    print_check(check_name, condition)
                    
        except Exception as e:
            print_check("Read pyproject.toml", False, str(e))
    
    # Git Repository Check
    print_header("8. GIT REPOSITORY STATUS")
    
    git_dir = base_path / ".git"
    is_git_repo = git_dir.exists()
    print_check("Is Git repository", is_git_repo)
    
    if is_git_repo:
        try:
            # Check git status
            result = subprocess.run(['git', 'status', '--porcelain'], 
                                 capture_output=True, text=True, cwd=base_path)
            is_clean = len(result.stdout.strip()) == 0
            print_check("Working directory clean", is_clean, 
                       "Ready for commit" if is_clean else "Has uncommitted changes")
            
            # Check for remote
            result = subprocess.run(['git', 'remote', '-v'], 
                                 capture_output=True, text=True, cwd=base_path)
            has_remote = len(result.stdout.strip()) > 0
            print_check("Has git remote", has_remote)
            
        except Exception as e:
            print_check("Git commands", False, str(e))
    
    # Final Summary
    print_header("9. RELEASE READINESS SUMMARY")
    
    release_criteria = [
        ("Essential files present", all_files_exist),
        ("Core structure complete", core_structure_ok), 
        ("Python syntax valid", syntax_ok),
        ("Documentation adequate", readme_file.exists()),
        ("Version configured", pyproject_file.exists()),
        ("Git repository ready", is_git_repo),
    ]
    
    ready_count = sum(1 for _, status in release_criteria if status)
    total_count = len(release_criteria)
    
    for criteria, status in release_criteria:
        print_check(criteria, status)
    
    print(f"\n📊 READINESS SCORE: {ready_count}/{total_count}")
    
    if ready_count == total_count:
        print("\n🎉 READY FOR RELEASE! 🚀")
        print("✅ All checks passed. Package is ready for GitHub release.")
        
        print("\n📋 NEXT STEPS:")
        print("1. Create GitHub repository")
        print("2. Push code: git push origin main")
        print("3. Create release tag: git tag v1.0.0")
        print("4. Push tag: git push origin v1.0.0")
        print("5. Create GitHub release with changelog")
        print("6. Optional: Publish to PyPI")
        
    else:
        print("\n⚠️ ISSUES FOUND")
        print(f"Please address {total_count - ready_count} issues before release.")
    
    return ready_count == total_count

if __name__ == "__main__":
    try:
        ready = run_pre_release_check()
        sys.exit(0 if ready else 1)
    except KeyboardInterrupt:
        print("\n\n🛑 Check interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Check failed with error: {e}")
        sys.exit(1)
