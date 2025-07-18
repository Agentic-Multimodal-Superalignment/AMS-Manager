#!/usr/bin/env python3
"""
🧙‍♂️ Merlin CLI - Command Line Interface for AMS Manager

This module provides the command-line interface for Merlin,
including interactive modes and Open Interpreter integration.
"""

import argparse
import os
import sys
from pathlib import Path
from typing import Optional, List, Dict, Any
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
from rich.text import Text

try:
    from interpreter import interpreter
    INTERPRETER_AVAILABLE = True
except ImportError:
    INTERPRETER_AVAILABLE = False
    print("⚠️ Open Interpreter not available. Install with: pip install open-interpreter")


class MerlinCLI:
    """
    🧙‍♂️ The Command Line Interface for Merlin
    
    Provides both traditional CLI commands and interactive wizard modes.
    """
    
    def __init__(self, merlin_core=None):
        self.console = Console()
        self.merlin_core = merlin_core
        self.setup_interpreter()
        
    def setup_interpreter(self):
        """Configure Open Interpreter for Merlin's magical assistance"""
        if INTERPRETER_AVAILABLE:
            # Configure for local/offline use if desired
            interpreter.offline = False  # Can be configured
            interpreter.auto_run = False  # Always ask for confirmation
            
    def interactive_mode(self):
        """
        🧙‍♂️ Enter Merlin's Interactive Wizard Mode
        """
        self.console.print(Panel.fit(
            "[bold blue]🧙‍♂️ Merlin's Interactive Workshop[/bold blue]\n"
            "Choose your adventure, young apprentice!",
            border_style="blue"
        ))
        
        while True:
            self.console.print("\n[bold]What shall we do today?[/bold]")
            choices = [
                "1. 🔍 Detect current AI/ML installations",
                "2. 📦 Install new packages from manifest", 
                "3. 🎯 Smart install (only missing packages)",
                "4. 🤖 Ask Merlin anything (Open Interpreter)",
                "5. ⚙️  Configure AMS environment",
                "6. 📋 Show installation status",
                "7. 🚪 Exit"
            ]
            
            for choice in choices:
                self.console.print(choice)
                
            selection = Prompt.ask("\nYour choice", choices=["1", "2", "3", "4", "5", "6", "7"])
            
            if selection == "1":
                self.detect_installations()
            elif selection == "2":
                self.install_from_manifest()
            elif selection == "3":
                self.smart_install()
            elif selection == "4":
                self.chat_with_merlin()
            elif selection == "5":
                self.configure_environment()
            elif selection == "6":
                self.show_status()
            elif selection == "7":
                self.console.print("🧙‍♂️ May your models converge and your gradients flow! Farewell!")
                break
                
    def detect_installations(self):
        """Detect what's already installed in the user's environment"""
        self.console.print("\n🔍 [bold]Scanning for existing installations...[/bold]")
        
        # This will be implemented with the environment detector
        if self.merlin_core:
            detected = self.merlin_core.detect_installations()
            self.display_detection_results(detected)
        else:
            self.console.print("⚠️ Merlin core not initialized!")
            
    def install_from_manifest(self):
        """Install packages from the manifest"""
        self.console.print("\n📦 [bold]Installing from manifest...[/bold]")
        
        manifest_path = Prompt.ask(
            "Manifest path", 
            default="src/ams_manager/config/ams_manifest.json"
        )
        
        if self.merlin_core:
            self.merlin_core.install_from_manifest(manifest_path)
        else:
            self.console.print("⚠️ Merlin core not initialized!")
            
    def smart_install(self):
        """Intelligently install only what's missing"""
        self.console.print("\n🎯 [bold]Smart Installation Mode[/bold]")
        self.console.print("Let me check what you have and install only what's missing...")
        
        if self.merlin_core:
            missing_packages = self.merlin_core.find_missing_packages()
            if missing_packages:
                self.console.print(f"\nFound {len(missing_packages)} missing packages:")
                for pkg in missing_packages:
                    self.console.print(f"  • {pkg}")
                    
                if Confirm.ask("Shall I install these for you?"):
                    self.merlin_core.install_packages(missing_packages)
            else:
                self.console.print("✨ Everything appears to be installed already!")
        else:
            self.console.print("⚠️ Merlin core not initialized!")
            
    def chat_with_merlin(self):
        """Enter Open Interpreter chat mode as Merlin"""
        if not INTERPRETER_AVAILABLE:
            self.console.print("⚠️ Open Interpreter not available. Please install it first.")
            return
            
        self.console.print(Panel.fit(
            "[bold blue]🧙‍♂️ Merlin's Magical Chat Mode[/bold blue]\n"
            "Ask me anything about AMS, installations, or let me help with tasks!\n"
            "Type 'exit' to return to the main menu.",
            border_style="blue"
        ))
        
        # Set up Merlin's personality in the interpreter
        merlin_context = """
        You are Merlin, a wise wizard and AI assistant specializing in AI/ML tools and the AMS framework.
        You can help with installations, configurations, debugging, and general AI/ML questions.
        You have access to the AMS Manager tools and can execute commands to help the user.
        Be helpful, wise, and occasionally use wizard-themed language.
        """
        
        while True:
            user_input = Prompt.ask("\n🧙‍♂️ Ask Merlin")
            if user_input.lower() in ['exit', 'quit', 'back']:
                break
                
            try:
                # Add Merlin context to the conversation
                full_prompt = f"{merlin_context}\n\nUser question: {user_input}"
                response = interpreter.chat(full_prompt)
                # The response will be streamed automatically by Open Interpreter
            except Exception as e:
                self.console.print(f"⚠️ Error communicating with Merlin: {e}")
                
    def configure_environment(self):
        """Configure the AMS environment settings"""
        self.console.print("\n⚙️ [bold]Environment Configuration[/bold]")
        
        # Get current settings or defaults
        current_home = os.environ.get('AIML_PROJECTS_HOME', str(Path.home() / 'aiml_projects'))
        
        self.console.print(f"Current AIML_PROJECTS_HOME: {current_home}")
        
        new_home = Prompt.ask(
            "Set new AIML_PROJECTS_HOME directory",
            default=current_home
        )
        
        if new_home != current_home:
            # Create directory if it doesn't exist
            Path(new_home).mkdir(parents=True, exist_ok=True)
            
            # Update environment variable
            os.environ['AIML_PROJECTS_HOME'] = new_home
            
            self.console.print(f"✅ Updated AIML_PROJECTS_HOME to: {new_home}")
            
            # Ask if they want to make it permanent
            if Confirm.ask("Make this permanent by adding to your shell profile?"):
                self.add_to_shell_profile('AIML_PROJECTS_HOME', new_home)
                
    def add_to_shell_profile(self, var_name: str, var_value: str):
        """Add environment variable to shell profile"""
        # This is a simplified version - could be enhanced
        profile_files = [
            Path.home() / '.bashrc',
            Path.home() / '.zshrc',
            Path.home() / '.profile'
        ]
        
        export_line = f'export {var_name}="{var_value}"\n'
        
        for profile in profile_files:
            if profile.exists():
                with open(profile, 'a') as f:
                    f.write(f'\n# Added by Merlin AMS Manager\n{export_line}')
                self.console.print(f"✅ Added to {profile}")
                break
        else:
            self.console.print("⚠️ No shell profile found. You may need to add this manually.")
            
    def install_packages(self, package_names: list):
        """Install specific packages"""
        self.console.print(f"\n📦 [bold]Installing packages: {', '.join(package_names)}[/bold]")
        
        if self.merlin_core:
            self.merlin_core.install_packages(package_names)
        else:
            self.console.print("⚠️ Merlin core not initialized!")
    
    def show_status(self):
        """Show current installation status"""
        self.console.print("\n📋 [bold]Installation Status[/bold]")
        
        if self.merlin_core:
            status = self.merlin_core.get_installation_status()
            self.display_installation_status(status)
        else:
            self.console.print("⚠️ Merlin core not initialized!")
    
    def display_installation_status(self, status: dict):
        """Display installation status in a nice format"""
        from rich.table import Table
        
        table = Table(title="🧙‍♂️ Merlin's Installation Status")
        table.add_column("Tool", style="cyan")
        table.add_column("Status", style="green")
        table.add_column("Location", style="dim")
        table.add_column("Version", style="blue")
        
        for package_name, info in status.items():
            status_text = "✅ Installed" if info.get('installed', False) else "❌ Missing"
            location = info.get('path', 'N/A')
            version = info.get('version', 'Unknown')
            
            table.add_row(package_name, status_text, location, version)
        
        self.console.print(table)
        
        # Show summary
        installed_count = sum(1 for info in status.values() if info.get('installed', False))
        total_count = len(status)
        
        self.console.print(f"\n📊 Summary: {installed_count}/{total_count} tools installed")
        
        if installed_count < total_count:
            missing = [name for name, info in status.items() if not info.get('installed', False)]
            self.console.print(f"💡 Missing tools: {', '.join(missing)}")
            self.console.print("🚀 Run 'smart-install' to install missing packages!")

    def display_detection_results(self, detected: dict):
        """Display detection results in a nice format"""
        from rich.table import Table
        
        table = Table(title="🔍 Environment Detection Results")
        table.add_column("Tool", style="cyan")
        table.add_column("Status", style="green")
        table.add_column("Location", style="dim")
        table.add_column("Details", style="blue")
        
        for tool_name, info in detected.items():
            if info.installed:
                status = "✅ Found"
                location = info.path or "System"
                details = f"v{info.version}" if info.version else "Detected"
            else:
                status = "❌ Missing"
                location = "Not found"
                details = "Available for install"
            
            table.add_row(tool_name, status, location, details)
        
        self.console.print(table)

    def run_from_args(self, args: List[str]):
        """Run CLI commands from command line arguments"""
        parser = argparse.ArgumentParser(
            description="🧙‍♂️ Merlin - Your AMS Assistant",
            epilog="For interactive mode, run without arguments"
        )
        
        parser.add_argument(
            "command",
            choices=["detect", "install", "smart-install", "chat", "config", "status"],
            help="Command to run"
        )
        
        parser.add_argument(
            "--manifest",
            default="src/ams_manager/config/ams_manifest.json",
            help="Path to manifest file"
        )
        
        parser.add_argument(
            "--profile",
            default="default",
            help="Configuration profile to use"
        )
        
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show what would be done without executing"
        )
        
        parser.add_argument(
            "--home-dir",
            help="Set AIML_PROJECTS_HOME directory"
        )
        
        parsed_args = parser.parse_args(args)
        
        # Execute the requested command
        if parsed_args.command == "detect":
            self.detect_installations()
        elif parsed_args.command == "install":
            self.install_from_manifest()
        elif parsed_args.command == "smart-install":
            self.smart_install()
        elif parsed_args.command == "chat":
            self.chat_with_merlin()
        elif parsed_args.command == "config":
            self.configure_environment()
        elif parsed_args.command == "status":
            self.show_status()