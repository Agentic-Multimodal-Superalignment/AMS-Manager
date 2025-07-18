# 🧙‍♂️ Merlin - AMS Manager

*Your magical assistant for AI/ML tool management with Open Interpreter & Ollama integration*

```
    🧙‍♂️
   /|\  "Greetings! I am Merlin, your wise assistant
  / | \  for navigating the realm of AI tools.
 ✨ ⚡ ✨ Let me help you build something magical!"
```

## ✨ What is Merlin?

Merlin is an intelligent, modular assistant that transforms complex AI/ML tool management into a magical experience. Built with **Open Interpreter** and **Ollama** integration, Merlin provides:

### 🎯 **Core Capabilities**
- 🔍 **Intelligent Detection** - Automatically scans and detects existing AI/ML installations
- 📦 **Modular Installation** - Smart install from GitHub, HuggingFace, or custom repositories  
- 🧙‍♂️ **Auto-Configuration** - Uses LLM to read README and auto-configure installation steps
- 📋 **Manifest Management** - Create, share, import/export tool collections
- 🤖 **Documentation Querying** - Ask questions about any installed project's docs and code
- 🦙 **Ollama Integration** - 67+ local models with hot-swapping and recommendations
- 🗣️ **Natural Language Control** - Chat interface for all operations
- ⚙️ **Environment Management** - UV/venv support with proper isolation

## 🚀 Quick Start

### Prerequisites
- Python 3.8+ (3.10+ recommended for best Ollama integration)
- Git
- [Ollama](https://ollama.ai) (for LLM integration)
- 8GB+ RAM (16GB+ recommended for AI tools)
- UV package manager (recommended) or pip

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/your-username/merlin-ams-manager.git
cd merlin-ams-manager
```

2. **Create virtual environment:**
```bash
# Using UV (recommended)
uv venv -p 3.11 .venv
.venv\Scripts\activate

# Or using Python venv
python -m venv .venv
.venv\Scripts\activate
```

3. **Install dependencies:**

#### Option A: Modern Installation (Recommended)
```bash
# Install from pyproject.toml (includes all dependencies)
uv pip install -e .

# Or install with optional features
uv pip install -e ".[full,dev]"
```

#### Option B: Traditional Installation
```bash
# Using UV
uv pip install -r requirements.txt

# Or using pip
pip install -r requirements.txt
```

4. **Install Ollama and models:**
```bash
# Install Ollama from https://ollama.ai
# Pull some useful models
ollama pull llama3.2
ollama pull qwen2.5-coder
ollama pull deepseek-coder
```

5. **Set your projects directory (optional):**
```bash
# Windows
set AIML_PROJECTS_HOME=M:\AMS\aiml_projects_home

# Linux/Mac
export AIML_PROJECTS_HOME=/path/to/your/aiml_projects
```

6. **Run Merlin:**

#### Option A: Using CLI Entry Point (After Installation with -e .)
```bash
merlin --help
merlin status  # Check system status
merlin         # Interactive menu
```

#### Option B: Direct Python Execution
```bash
python src/ams_manager/main.py
```

## 🎯 Core Features

## 🎯 Core Features

### 🔍 **Intelligent Detection**
- Automatically scans your system for existing AI/ML tools
- Detects ComfyUI, FluxGym, Open WebUI, OneTrainer, and more
- Shows installation status and locations

### 📦 **Modular Installation System**
- **GitHub/HuggingFace Integration**: Install any public repository
- **Auto-Configuration**: Uses LLM to read README and configure installs
- **Manifest-Based**: Create collections of tools for easy sharing
- **Environment Isolation**: Proper virtual environment management

### 🧙‍♂️ **Auto-Configuration Magic**
```bash
# Auto-configure any repository
python main.py --add-repo "https://github.com/username/awesome-ai-tool"
```
Merlin will:
1. Read the repository's README and documentation
2. Extract installation commands and requirements
3. Configure proper virtual environment settings
4. Set up start commands and web interfaces

### 📋 **Manifest Management**
- **Create**: Build manifests from installed tools
- **Export**: Share your tool collections with others
- **Import**: Install complete toolsets from shared manifests
- **Version Control**: Track installation metadata

### 🤖 **Documentation Querying**
Ask questions about any installed project:
```bash
# Query project documentation
python main.py query --tool "ComfyUI" --question "How do I install custom nodes?"

# Interactive docs mode
python main.py docs
```

### 🦙 **Ollama Model Management**
- **67+ Models**: Automatic detection of installed Ollama models
- **Smart Recommendations**: Get coding, documentation, or general-purpose model suggestions
- **Hot-Swapping**: Change models mid-session for different tasks
- **Configuration**: Set temperature and model preferences

```bash
# List available models
python main.py models

# Check current model status
python main.py model-status

# Configure default model
python main.py configure-model --model "qwen2.5-coder:latest" --temperature 0.1

# Hot-swap for current session
python main.py hot-swap --model "deepseek-coder:latest"
```

### 🗣️ **Natural Language Interface**
Interactive chat mode for natural language commands:
```bash
python main.py chat
```
Or use the interactive menu:
```bash
python main.py
```

## 🛠️ Command Line Interface

### Basic Commands
```bash
# Interactive menu
python main.py

# Check tool status
python main.py status

# Install specific tools
python main.py install

# Chat with Merlin
python main.py chat

# Manage manifests
python main.py manifests

# Documentation assistant
python main.py docs

# Model management
python main.py models
```

### Advanced Commands
```bash
# Set custom AIML home directory
python main.py --aiml-home "/custom/path" status

# Auto-configure and install a repository
python main.py --add-repo "https://github.com/user/repo.git"

# Query specific tool documentation
python main.py query --tool "tool-name" --question "How do I use this?"

# Configure model with specific temperature
python main.py configure-model --model "llama3.2:latest" --temperature 0.2
```
Merlin scans your system to find existing AI/ML tools:
```bash
python src/ams_manager/main.py detect
```

### 📦 Smart Installation
Install only what's missing with AI-powered decisions:
```bash
python src/ams_manager/main.py smart-install
```

### 🤖 Natural Language Assistant
Chat with Merlin using Open Interpreter:
```bash
python src/ams_manager/main.py chat
```

### 📋 Supported Tools

| Tool | Category | Description |
|------|----------|-------------|
| **ComfyUI** | Image Generation | Node-based Stable Diffusion interface |
| **Open WebUI** | LLM Interface | ChatGPT-like web interface for local models |
| **Flux Gym** | Model Training | Easy training interface for Flux models |
| **Automatic1111** | Image Generation | Popular Stable Diffusion WebUI |
| **InvokeAI** | Image Generation | Professional AI art generation |
| **JupyterLab** | Development | Interactive development environment |

## 🧙‍♂️ Using Merlin

### Interactive Mode
```bash
python src/ams_manager/main.py
```

This launches Merlin's interactive wizard where you can:
1. Detect current installations
2. Install new packages  
3. Run smart install (only missing tools)
4. Chat with Merlin (Open Interpreter)
5. Configure environment
6. View status

### Command Line Mode
```bash
# Detect installations
python src/ams_manager/main.py detect

# Install specific manifest
python src/ams_manager/main.py install --manifest path/to/manifest.json

# Smart install (only missing)
python src/ams_manager/main.py smart-install

# Chat with Merlin
python src/ams_manager/main.py chat

# Configure environment
python src/ams_manager/main.py config --home-dir /path/to/aiml/projects
```

### Open Interpreter Integration

Merlin integrates seamlessly with Open Interpreter for natural language control:

```python
# In Open Interpreter chat
"Merlin, what AI tools do I have installed?"

"Please install ComfyUI for me"

"Show me the status of all my AI tools"

"Help me set up a stable diffusion workspace"
```

## ⚙️ Configuration

### Environment Setup
Merlin uses `AIML_PROJECTS_HOME` to organize your AI tools:

```bash
# Set custom location
export AIML_PROJECTS_HOME="/path/to/your/ai/projects"

# Or let Merlin configure it
python src/ams_manager/main.py config
```

### Manifest Customization
Edit `src/ams_manager/config/ams_manifest.json` to customize:
- Available packages
- Installation profiles (minimal, default, full)
- Package priorities
- System requirements

### Configuration Profiles
- **minimal**: Just ComfyUI
- **default**: ComfyUI + Open WebUI + Flux Gym  
- **full**: All available tools
- **development**: Development-focused tools

## 🔧 Development

### Project Structure
```
AMS-MANAGER/
├── src/ams_manager/
│   ├── core/                     # Core functionality
│   │   ├── manifest_manager.py   # Manifest and Ollama integration
│   │   ├── modular_installer.py  # Installation system
│   │   ├── documentation_manager.py # Doc querying
│   │   └── environment_detector.py  # Tool detection
│   ├── cli/                      # Command line interface
│   ├── api/                      # Future API endpoints
│   ├── utils/                    # Utility functions
│   └── main.py                   # Main entry point
├── docs/                         # Documentation
├── examples/                     # Usage examples
└── tests/                        # Test suite
```

### Key Components

#### 🧙‍♂️ **ManifestManager** (`manifest_manager.py`)
The heart of Merlin's intelligence:
- **Ollama Integration**: Auto-detects and configures 67+ local models
- **Auto-Configuration**: Uses LLM to read repositories and extract install info
- **Manifest Operations**: Create, load, export, import tool collections
- **Documentation Querying**: Ask questions about installed project docs
- **Model Management**: Hot-swap