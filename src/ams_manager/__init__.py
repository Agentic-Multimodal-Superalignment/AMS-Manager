#!/usr/bin/env python3
"""
🧙‍♂️ Merlin - AMS Manager

Your magical assistant for AI/ML tool management with Open Interpreter & Ollama integration.

This package provides:
- Intelligent AI/ML tool detection and installation
- Modular installation from GitHub, HuggingFace, and custom sources
- Open Interpreter integration for natural language control
- Ollama model management and hot-swapping
- Documentation querying and auto-configuration
- Manifest-based tool collections for sharing
"""

__version__ = "1.0.0"
__author__ = "Merlin AMS Manager Team"
__email__ = "your-email@example.com"
__description__ = "🧙‍♂️ Magical AI/ML tool management with Open Interpreter & Ollama"

# Core imports for easy access
try:
    from .core.manifest_manager import ManifestManager, ToolConfig, SourceType
    from .core.modular_installer import ModularInstaller
    from .core.documentation_manager import DocumentationManager
    from .core.merlin_core import MerlinCore
    
    __all__ = [
        "ManifestManager",
        "ToolConfig", 
        "SourceType",
        "ModularInstaller",
        "DocumentationManager",
        "MerlinCore",
    ]
except ImportError:
    # Handle cases where dependencies aren't installed
    __all__ = []

def get_version():
    """Get the current version"""
    return __version__

def main():
    """Main entry point for the CLI"""
    from .main import main as cli_main
    cli_main()

if __name__ == "__main__":
    main()
