# Changelog

All notable changes to Merlin AMS Manager will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-01-18

### Added
- 🧙‍♂️ **Core AMS Manager System**
  - Intelligent AI/ML tool detection and management
  - Modular installation system for GitHub/HuggingFace repositories
  - Manifest-based tool collections for easy sharing
  - Environment isolation with UV/venv support

- 🦙 **Ollama Integration**
  - Auto-detection of 67+ local Ollama models
  - Model recommendations by use case (coding, documentation, general, fast)
  - Hot-swapping between models during sessions
  - OpenAI-compatible API configuration

- 🤖 **Open Interpreter Integration**
  - Natural language control of all operations
  - Auto-configuration using LLM to read README files
  - Documentation querying for installed projects
  - Intelligent installation instruction extraction

- 📋 **Manifest Management**
  - Create, load, export, and import tool manifests
  - Share tool collections with others
  - Support for multiple source types (GitHub, HuggingFace, custom)
  - Automatic metadata tracking

- 🔍 **Tool Detection**
  - Automatic scanning for existing AI/ML installations
  - Support for ComfyUI, FluxGym, OneTrainer, Open WebUI, and more
  - Path detection and configuration status reporting

- 🖥️ **CLI Interface**
  - Interactive menu system
  - Command-line arguments for automation
  - Rich terminal output with emojis and colors
  - Status reporting and progress indicators

- 📚 **Documentation System**
  - Project documentation querying
  - Code analysis and usage examples
  - README parsing and knowledge base creation
  - Context-aware help system

### Technical Features
- Python 3.8+ compatibility
- Modern packaging with pyproject.toml
- Comprehensive test suite
- Type hints and documentation
- Error handling and graceful degradation
- Cross-platform support (Windows, macOS, Linux)

### Configuration
- Environment variable support for AIML_PROJECTS_HOME
- YAML configuration files
- JSON manifest format
- Customizable installation profiles

### Dependencies
- Core: pyyaml, rich, requests, click
- Optional: open-interpreter for LLM features
- Development: pytest, black, isort, mypy

### Known Issues
- Open Interpreter required for auto-configuration features
- Ollama must be running locally for model management
- Large AI tools require significant disk space

### Documentation
- Comprehensive README with setup instructions
- API documentation and examples
- Testing report with validation results
- Development setup and contribution guidelines
