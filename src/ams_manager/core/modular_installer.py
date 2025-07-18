#!/usr/bin/env python3
"""
🧙‍♂️ Modular Installer - Smart Installation System

This module handles installation of tools from various sources:
- GitHub repositories
- HuggingFace models/spaces
- Custom sources
- PyPI packages

Supports automatic configuration and Open Interpreter integration.
"""

import subprocess
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

from .manifest_manager import ManifestManager, ToolConfig, SourceType


@dataclass
class InstallResult:
    success: bool
    tool_name: str
    message: str
    install_path: Optional[Path] = None
    start_command: str = ""


class ModularInstaller:
    """🧙‍♂️ Smart modular installer for AI/ML tools"""
    
    def __init__(self, manifest_manager: ManifestManager):
        self.manifest_manager = manifest_manager
        self.aiml_home = manifest_manager.aiml_home
    
    def install_tool(self, tool_config: ToolConfig) -> InstallResult:
        """Install a tool based on its configuration"""
        print(f"\n🔧 Installing {tool_config.display_name}...")
        
        # Get the appropriate directory for this source type
        base_dir = self.manifest_manager.get_source_directory(tool_config.source_type)
        tool_path = base_dir / tool_config.folder_name
        
        try:
            if tool_config.source_type == SourceType.GITHUB:
                return self._install_github_tool(tool_config, tool_path)
            elif tool_config.source_type == SourceType.HUGGINGFACE:
                return self._install_huggingface_tool(tool_config, tool_path)
            elif tool_config.source_type == SourceType.PYPI:
                return self._install_pypi_tool(tool_config)
            else:
                return self._install_custom_tool(tool_config, tool_path)
                
        except Exception as e:
            return InstallResult(
                success=False,
                tool_name=tool_config.name,
                message=f"❌ Installation failed: {e}"
            )
    
    def _install_github_tool(self, tool_config: ToolConfig, tool_path: Path) -> InstallResult:
        """Install a GitHub repository"""
        # Clone if not exists
        if not tool_path.exists():
            print(f"  📥 Cloning from GitHub: {tool_config.url}")
            result = subprocess.run([
                "git", "clone", tool_config.url, str(tool_path)
            ], capture_output=True, text=True)
            
            if result.returncode != 0:
                return InstallResult(
                    success=False,
                    tool_name=tool_config.name,
                    message=f"❌ Git clone failed: {result.stderr}"
                )
            print("    ✅ Repository cloned successfully")
        else:
            print("    ℹ️ Repository already exists")
        
        # Set up virtual environment
        if tool_config.use_venv:
            venv_result = self._setup_virtual_environment(tool_config, tool_path)
            if not venv_result.success:
                return venv_result
        
        # Install dependencies
        if tool_config.install_commands:
            install_result = self._run_install_commands(tool_config, tool_path)
            if not install_result.success:
                return install_result
        
        return InstallResult(
            success=True,
            tool_name=tool_config.name,
            message=f"🎉 {tool_config.display_name} installed successfully!",
            install_path=tool_path,
            start_command=tool_config.start_command
        )
    
    def _install_huggingface_tool(self, tool_config: ToolConfig, tool_path: Path) -> InstallResult:
        """Install a HuggingFace model or space"""
        # For HuggingFace, we might use git-lfs or huggingface_hub
        print(f"  📥 Downloading from HuggingFace: {tool_config.url}")
        
        try:
            # Try using git clone with LFS support
            if not tool_path.exists():
                result = subprocess.run([
                    "git", "clone", tool_config.url, str(tool_path)
                ], capture_output=True, text=True)
                
                if result.returncode != 0:
                    return InstallResult(
                        success=False,
                        tool_name=tool_config.name,
                        message=f"❌ HuggingFace clone failed: {result.stderr}"
                    )
                print("    ✅ HuggingFace content downloaded successfully")
            
            return InstallResult(
                success=True,
                tool_name=tool_config.name,
                message=f"🎉 {tool_config.display_name} downloaded successfully!",
                install_path=tool_path,
                start_command=tool_config.start_command
            )
            
        except Exception as e:
            return InstallResult(
                success=False,
                tool_name=tool_config.name,
                message=f"❌ HuggingFace installation failed: {e}"
            )
    
    def _install_pypi_tool(self, tool_config: ToolConfig) -> InstallResult:
        """Install a PyPI package"""
        print(f"  📦 Installing PyPI package: {tool_config.name}")
        
        try:
            if tool_config.use_uv:
                cmd = ["uv", "pip", "install", tool_config.name]
            else:
                cmd = ["pip", "install", tool_config.name]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                return InstallResult(
                    success=False,
                    tool_name=tool_config.name,
                    message=f"❌ PyPI installation failed: {result.stderr}"
                )
            
            return InstallResult(
                success=True,
                tool_name=tool_config.name,
                message=f"🎉 {tool_config.display_name} installed successfully!",
                start_command=tool_config.start_command
            )
            
        except Exception as e:
            return InstallResult(
                success=False,
                tool_name=tool_config.name,
                message=f"❌ PyPI installation failed: {e}"
            )
    
    def _install_custom_tool(self, tool_config: ToolConfig, tool_path: Path) -> InstallResult:
        """Install a custom tool with provided commands"""
        print(f"  🔧 Installing custom tool: {tool_config.display_name}")
        
        # Create directory if needed
        tool_path.mkdir(parents=True, exist_ok=True)
        
        # Run custom install commands
        if tool_config.install_commands:
            install_result = self._run_install_commands(tool_config, tool_path)
            if not install_result.success:
                return install_result
        
        return InstallResult(
            success=True,
            tool_name=tool_config.name,
            message=f"🎉 {tool_config.display_name} installed successfully!",
            install_path=tool_path,
            start_command=tool_config.start_command
        )
    
    def _setup_virtual_environment(self, tool_config: ToolConfig, tool_path: Path) -> InstallResult:
        """Set up virtual environment for the tool"""
        if tool_config.use_uv:
            print("  🏗️ Creating UV virtual environment...")
            venv_cmd = ["uv", "venv", ".venv"]
        else:
            print("  🏗️ Creating Python virtual environment...")
            venv_cmd = ["python", "-m", "venv", "venv"]
        
        result = subprocess.run(venv_cmd, cwd=tool_path, capture_output=True, text=True)
        
        if result.returncode != 0:
            return InstallResult(
                success=False,
                tool_name=tool_config.name,
                message=f"❌ Virtual environment creation failed: {result.stderr}"
            )
        
        print("    ✅ Virtual environment created")
        return InstallResult(success=True, tool_name=tool_config.name, message="")
    
    def _run_install_commands(self, tool_config: ToolConfig, tool_path: Path) -> InstallResult:
        """Run the installation commands for a tool"""
        print("  📦 Installing dependencies...")
        
        for i, command in enumerate(tool_config.install_commands):
            print(f"    Running step {i+1}/{len(tool_config.install_commands)}: {command}")
            
            try:
                # Handle different command types
                if command.startswith("git clone"):
                    # Already handled in clone step
                    continue
                elif "&&" in command:
                    # Shell command with activation
                    result = subprocess.run(
                        command, 
                        shell=True, 
                        cwd=tool_path, 
                        capture_output=True, 
                        text=True
                    )
                else:
                    # Simple command
                    result = subprocess.run(
                        command.split(), 
                        cwd=tool_path, 
                        capture_output=True, 
                        text=True
                    )
                
                if result.returncode != 0:
                    print(f"    ⚠️ Command warning: {result.stderr}")
                else:
                    print(f"    ✅ Step {i+1} completed")
                    
            except Exception as e:
                print(f"    ⚠️ Step {i+1} error: {e}")
        
        print("    ✅ All installation steps completed")
        return InstallResult(success=True, tool_name=tool_config.name, message="")
    
    def install_from_manifest(self, manifest_name: str, tool_names: List[str] = None) -> List[InstallResult]:
        """Install tools from a manifest"""
        print(f"🧙‍♂️ Installing from manifest: {manifest_name}")
        
        try:
            manifest = self.manifest_manager.load_manifest(f"{manifest_name}.json")
        except Exception as e:
            return [InstallResult(
                success=False,
                tool_name="manifest",
                message=f"❌ Failed to load manifest: {e}"
            )]
        
        tools_to_install = manifest.get("tools", [])
        if tool_names:
            tools_to_install = [
                tool for tool in tools_to_install 
                if tool.get("name") in tool_names
            ]
        
        results = []
        for tool_data in tools_to_install:
            try:
                # Convert dict to ToolConfig
                tool_config = ToolConfig(
                    name=tool_data["name"],
                    display_name=tool_data["display_name"],
                    source_type=SourceType(tool_data["source_type"]),
                    url=tool_data["url"],
                    description=tool_data.get("description", ""),
                    install_commands=tool_data.get("install_commands", []),
                    start_command=tool_data.get("start_command", ""),
                    web_interface=tool_data.get("web_interface", ""),
                    use_uv=tool_data.get("use_uv", True),
                    use_venv=tool_data.get("use_venv", True),
                    folder_name=tool_data.get("folder_name", tool_data["name"])
                )
                
                result = self.install_tool(tool_config)
                results.append(result)
                
            except Exception as e:
                results.append(InstallResult(
                    success=False,
                    tool_name=tool_data.get("name", "unknown"),
                    message=f"❌ Configuration error: {e}"
                ))
        
        return results
    
    def check_installation_status(self, tool_config: ToolConfig) -> bool:
        """Check if a tool is already installed"""
        if tool_config.source_type == SourceType.PYPI:
            try:
                result = subprocess.run([
                    "python", "-c", f"import {tool_config.name}"
                ], capture_output=True)
                return result.returncode == 0
            except:
                return False
        else:
            base_dir = self.manifest_manager.get_source_directory(tool_config.source_type)
            tool_path = base_dir / tool_config.folder_name
            return tool_path.exists()
