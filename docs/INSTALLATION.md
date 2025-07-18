# 📦 Installation Guide

## Modern Installation (Recommended)

The modern approach uses `pyproject.toml` which includes all dependency information in a single file:

```bash
# Clone the repository
git clone https://github.com/Agentic-Multimodal-Superalignment/AMS-Manager.git
cd AMS-Manager

# Install UV (if not already installed)
pip install uv

# Install in editable mode from pyproject.toml
uv pip install -e .

# This gives you the CLI command:
merlin --help
merlin status
```

### Optional Features

You can install optional features using the extras defined in `pyproject.toml`:

```bash
# Install with all optional features (Open Interpreter)
uv pip install -e ".[full]"

# Install with development tools
uv pip install -e ".[dev]"

# Install with both
uv pip install -e ".[full,dev]"
```

## Traditional Installation

If you prefer the traditional approach with `requirements.txt`:

```bash
# Clone the repository
git clone https://github.com/Agentic-Multimodal-Superalignment/AMS-Manager.git
cd AMS-Manager

# Install UV (if not already installed)
pip install uv

# Install from requirements.txt
uv pip install -r requirements.txt

# Run directly with Python
python src/ams_manager/main.py
```

## What's the Difference?

| Method | Dependencies | CLI Command | Development |
|--------|-------------|-------------|-------------|
| **Modern (`pyproject.toml`)** | ✅ All in one file | ✅ `merlin` command | ✅ Easy extras |
| **Traditional (`requirements.txt`)** | ⚠️ Separate file | ❌ Must use `python src/...` | ⚠️ Manual dev deps |

## Benefits of Modern Installation

1. **Single Source of Truth**: All dependencies, metadata, and configuration in `pyproject.toml`
2. **CLI Entry Point**: Get a convenient `merlin` command instead of typing the full path
3. **Optional Dependencies**: Easily install features like `[full]` or `[dev]` 
4. **Editable Installation**: Changes to code are immediately available without reinstalling
5. **Standard Python Packaging**: Follows modern Python packaging standards (PEP 517/518)

## Verification

After installation, verify everything works:

```bash
# Test the package import
python -c "import ams_manager; print('✅ Package imported successfully')"

# Test CLI (modern installation)
merlin --help

# Test direct execution (both methods)
python src/ams_manager/main.py --help
```

## PyPI Installation (Future)

Once published to PyPI, installation will be even simpler:

```bash
# Future PyPI installation
pip install merlin-ams-manager

# Or with UV
uv pip install merlin-ams-manager
```
