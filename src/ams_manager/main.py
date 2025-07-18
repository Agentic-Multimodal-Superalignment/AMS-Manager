#!/usr/bin/env python3
"""
🧙‍♂️ Merlin - Your SIMPLE AMS Assistant

Keep it simple! Just install tools and chat with Open Interpreter.
Now with modular installer support for GitHub/HuggingFace repos!
"""

import sys
import os
import argparse
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from interpreter import interpreter
    INTERPRETER_AVAILABLE = True
except ImportError:
    INTERPRETER_AVAILABLE = False
    print("⚠️ Open Interpreter not available. Install with: pip install open-interpreter")

from ams_manager.core.merlin_core import MerlinCore
from ams_manager.core.manifest_manager import ManifestManager, ToolConfig, SourceType
from ams_manager.core.modular_installer import ModularInstaller
from ams_manager.core.documentation_manager import DocumentationManager
from ams_manager.utils.environment_detector import SimpleEnvironmentDetector


def print_welcome():
    """Print Merlin's welcome message"""
    print("🧙‍♂️ " + "="*50)
    print("🧙‍♂️ Welcome to Merlin - Your Simple AMS Assistant!")
    print("🧙‍♂️ " + "="*50)
    print()
    print("✨ I help you install: ComfyUI, FluxGym, Open WebUI, OneTrainer")
    print("🔧 I can also install any GitHub or HuggingFace repo!")
    print("🎯 Set AIML_PROJECTS_HOME environment variable for your projects")
    print("🤖 Chat with me using Open Interpreter for natural language commands")
    print()


def initialize_merlin(aiml_home=None):
    """Initialize Merlin's modular system"""
    if aiml_home is None:
        aiml_home = os.environ.get('AIML_PROJECTS_HOME', str(Path.home() / 'aiml_projects'))
    
    aiml_path = Path(aiml_home)
    aiml_path.mkdir(exist_ok=True)
    
    # Initialize managers
    manifest_manager = ManifestManager(aiml_path)
    modular_installer = ModularInstaller(manifest_manager)
    
    return manifest_manager, modular_installer


def show_tools_status():
    """Show what tools are installed"""
    print("🔍 Scanning for installed tools...")
    
    # Get AIML_PROJECTS_HOME
    aiml_home = os.environ.get('AIML_PROJECTS_HOME', str(Path.home() / 'aiml_projects'))
    print(f"📁 Scanning directory: {aiml_home}")
    
    detector = SimpleEnvironmentDetector()
    tools = detector.scan_for_ai_tools()
    
    print("\n📦 Tool Status:")
    for tool_name, info in tools.items():
        status = "✅ Found" if info['found'] else "❌ Not Found"
        print(f"   {status} {tool_name}")
        if info['found'] and info['locations']:
            print(f"      → {info['locations'][0]}")
    print()


def select_tools_to_install():
    """Let user select tools to install or add custom repo"""
    tools = ['comfyui', 'fluxgym', 'open-webui', 'onetrainer']
    
    print("🧙‍♂️ Which tools would you like to install?")
    print()
    
    for i, tool in enumerate(tools, 1):
        print(f"{i}. {tool}")
    
    print("5. Add custom GitHub/HuggingFace repo")
    print("6. Install from manifest")
    
    print("\nEnter numbers (e.g., 1,3) or 'all' for everything:")
    selection = input("🧙‍♂️ Your choice: ").strip().lower()
    
    if selection == 'all':
        return {'type': 'default', 'tools': tools}
    elif selection == '5':
        return {'type': 'custom'}
    elif selection == '6':
        return {'type': 'manifest'}
    
    try:
        indices = [int(x.strip()) for x in selection.split(',')]
        selected = [tools[i-1] for i in indices if 1 <= i <= len(tools)]
        return {'type': 'default', 'tools': selected}
    except:
        print("❌ Invalid selection")
        return {'type': 'invalid'}


def install_tools(selection):
    """Install the selected tools using the modular installer"""
    manifest_manager, modular_installer = initialize_merlin()
    
    if selection['type'] == 'default':
        install_default_tools(selection['tools'], modular_installer)
    elif selection['type'] == 'custom':
        install_custom_repo(manifest_manager, modular_installer)
    elif selection['type'] == 'manifest':
        install_from_manifest_menu(manifest_manager, modular_installer)


def install_default_tools(selected_tools, modular_installer):
    """Install default tools using modular installer"""
    # Create tool configs for default tools
    default_configs = {
        'comfyui': ToolConfig(
            name='comfyui',
            display_name='ComfyUI',
            source_type=SourceType.GITHUB,
            url='https://github.com/comfyanonymous/ComfyUI.git',
            description='Powerful and modular stable diffusion GUI and backend',
            install_commands=[
                'uv venv .venv',
                '.venv\\Scripts\\uv pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu128',
                '.venv\\Scripts\\uv pip install -r requirements.txt'
            ],
            start_command='.venv\\Scripts\\python main.py',
            web_interface='http://localhost:8188',
            folder_name='ComfyUI'
        ),
        'fluxgym': ToolConfig(
            name='fluxgym',
            display_name='FluxGym',
            source_type=SourceType.GITHUB,
            url='https://github.com/cocktailpeanut/fluxgym.git',
            description='Flux model training environment',
            install_commands=[
                'git clone -b sd3 https://github.com/kohya-ss/sd-scripts',
                'uv venv env',
                'env\\Scripts\\activate && cd sd-scripts && uv pip install -r requirements.txt',
                'env\\Scripts\\activate && cd .. && uv pip install -r requirements.txt',
                'env\\Scripts\\activate && uv pip install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121'
            ],
            start_command='env\\Scripts\\python app.py',
            folder_name='fluxgym'
        ),
        'open-webui': ToolConfig(
            name='open-webui',
            display_name='Open WebUI',
            source_type=SourceType.PYPI,
            url='https://pypi.org/project/open-webui/',
            description='User-friendly WebUI for LLMs',
            install_commands=[],
            start_command='open-webui',
            web_interface='http://localhost:8080',
            use_venv=False
        ),
        'onetrainer': ToolConfig(
            name='onetrainer',
            display_name='OneTrainer',
            source_type=SourceType.GITHUB,
            url='https://github.com/Nerogar/OneTrainer.git',
            description='One trainer for diffusion models',
            install_commands=[
                'python -m venv venv',
                'venv\\Scripts\\pip install -r requirements.txt'
            ],
            start_command='venv\\Scripts\\python scripts\\train_ui.py',
            use_uv=False,  # OneTrainer has Git editable requirements
            folder_name='OneTrainer'
        )
    }
    
    for tool_name in selected_tools:
        if tool_name in default_configs:
            config = default_configs[tool_name]
            print(f"\n🔧 Installing {config.display_name}...")
            result = modular_installer.install_tool(config)
            print(result.message)
        else:
            print(f"❌ Unknown tool: {tool_name}")


def install_custom_repo(manifest_manager, modular_installer):
    """Install a custom GitHub or HuggingFace repository"""
    print("\n🧙‍♂️ Adding custom repository...")
    
    url = input("Enter GitHub/HuggingFace URL: ").strip()
    name = input("Enter name (or press Enter for auto-detect): ").strip()
    
    if not url:
        print("❌ URL is required")
        return
    
    # Auto-configure using Open Interpreter if available
    print("🔮 Auto-configuring repository...")
    tool_config = manifest_manager.auto_configure_tool(url, name or None)
    
    if tool_config:
        print(f"✅ Configuration complete for {tool_config.display_name}")
        print(f"📄 Description: {tool_config.description}")
        
        # Ask user to confirm installation
        confirm = input("\n🧙‍♂️ Install this tool? (y/n): ").strip().lower()
        if confirm == 'y':
            result = modular_installer.install_tool(tool_config)
            print(result.message)
        else:
            print("Installation cancelled")
    else:
        print("❌ Failed to configure repository")


def install_from_manifest_menu(manifest_manager, modular_installer):
    """Show available manifests and install from selected one"""
    manifests = manifest_manager.list_manifests()
    
    if not manifests:
        print("❌ No manifests found")
        return
    
    print("\n🧙‍♂️ Available manifests:")
    for i, manifest in enumerate(manifests, 1):
        print(f"{i}. {manifest['name']} - {manifest['tools_count']} tools")
        print(f"   {manifest['description']}")
    
    try:
        selection = int(input("\nSelect manifest number: ")) - 1
        if 0 <= selection < len(manifests):
            manifest_name = manifests[selection]['file'].replace('.json', '')
            results = modular_installer.install_from_manifest(manifest_name)
            
            for result in results:
                print(result.message)
        else:
            print("❌ Invalid selection")
    except ValueError:
        print("❌ Invalid input")


def manage_manifests_menu():
    """Manage manifests - list, export, import"""
    manifest_manager, _ = initialize_merlin()
    
    while True:
        print("\n🧙‍♂️ Manifest Management")
        print("1. List manifests")
        print("2. Export manifests")
        print("3. Import manifests")
        print("4. Back to main menu")
        
        choice = input("\nChoose option (1-4): ").strip()
        
        if choice == '1':
            manifests = manifest_manager.list_manifests()
            if manifests:
                print("\n📦 Available manifests:")
                for manifest in manifests:
                    print(f"  📄 {manifest['name']} - {manifest['tools_count']} tools")
                    print(f"     {manifest['description']}")
                    print(f"     Sources: {', '.join(manifest['source_types'])}")
            else:
                print("❌ No manifests found")
                
        elif choice == '2':
            manifests = manifest_manager.list_manifests()
            if manifests:
                print("\nSelect manifests to export (comma-separated numbers) or 'all':")
                for i, manifest in enumerate(manifests, 1):
                    print(f"{i}. {manifest['name']}")
                
                selection = input("Selection: ").strip()
                if selection.lower() == 'all':
                    manifest_names = [m['file'].replace('.json', '') for m in manifests]
                else:
                    try:
                        indices = [int(x.strip()) for x in selection.split(',')]
                        manifest_names = [manifests[i-1]['file'].replace('.json', '') for i in indices if 1 <= i <= len(manifests)]
                    except:
                        print("❌ Invalid selection")
                        continue
                
                export_file = input("Export filename (press Enter for 'exported_manifests.json'): ").strip()
                if not export_file:
                    export_file = "exported_manifests.json"
                
                export_path = Path(export_file)
                manifest_manager.export_manifests(export_path, manifest_names)
                print(f"✅ Exported to {export_path}")
            else:
                print("❌ No manifests to export")
                
        elif choice == '3':
            import_file = input("Import filename: ").strip()
            if import_file and Path(import_file).exists():
                overwrite = input("Overwrite existing manifests? (y/n): ").strip().lower() == 'y'
                imported = manifest_manager.import_manifests(Path(import_file), overwrite)
                print(f"✅ Imported {len(imported)} manifests")
            else:
                print("❌ File not found")
                
        elif choice == '4':
            break
        else:
            print("❌ Invalid choice")


def chat_with_merlin():
    """Chat with Merlin using Open Interpreter"""
    if not INTERPRETER_AVAILABLE:
        print("❌ Open Interpreter not available!")
        print("💡 Install with: pip install open-interpreter")
        return
    
    # Set up Merlin's personality
    interpreter.custom_instructions = """
    You are Merlin, a wise wizard assistant for AI/ML tool management. 
    You help users install and manage ComfyUI, FluxGym, Open WebUI, OneTrainer, and any GitHub/HuggingFace repositories.
    You're helpful, wise, and occasionally use wizard-themed language.
    The user's AI/ML tools are located in their AIML_PROJECTS_HOME directory.
    You can help with installations, troubleshooting, and general AI/ML questions.
    You have access to a modular installer that can handle any GitHub or HuggingFace repository automatically.
    """
    
    # Show current environment
    print("🧙‍♂️ Greetings! Let me first check your current setup...")
    show_tools_status()
    
    print("🤖 You can now chat with me! Ask me anything about your AI/ML tools.")
    print("💡 Try: 'Install ComfyUI' or 'Add this GitHub repo: https://github.com/...'")
    print()
    
    interpreter.chat()


def scan_documentation():
    """Scan and analyze documentation for all installed tools"""
    aiml_home = os.environ.get('AIML_PROJECTS_HOME', str(Path.home() / 'aiml_projects'))
    docs_manager = DocumentationManager(Path(aiml_home))
    
    print("📚 Scanning documentation for all installed tools...")
    documentation = docs_manager.scan_installed_tools()
    
    print(f"\n📖 Documentation Summary:")
    for tool_name, doc_entry in documentation.items():
        print(f"  📦 {tool_name}")
        print(f"     README: {'✅' if doc_entry.readme_content else '❌'}")
        print(f"     Docs: {len(doc_entry.docs_files)} files")
        print(f"     Examples: {len(doc_entry.code_examples)} found")
        print(f"     Usage: {'✅' if doc_entry.usage_instructions else '❌'}")
        print()


def query_tool_docs(tool_name: str, question: str):
    """Query documentation for a specific tool"""
    aiml_home = os.environ.get('AIML_PROJECTS_HOME', str(Path.home() / 'aiml_projects'))
    docs_manager = DocumentationManager(Path(aiml_home))
    
    print(f"🔍 Querying {tool_name} documentation...")
    answer = docs_manager.query_tool_documentation(tool_name, question)
    print(f"\n📚 Answer for '{question}':")
    print(answer)


def docs_interactive_mode():
    """Interactive documentation query mode"""
    if not INTERPRETER_AVAILABLE:
        print("❌ Open Interpreter required for documentation queries")
        return
    
    aiml_home = os.environ.get('AIML_PROJECTS_HOME', str(Path.home() / 'aiml_projects'))
    docs_manager = DocumentationManager(Path(aiml_home))
    
    print("📚 Documentation Interactive Mode")
    print("=" * 40)
    
    # Scan documentation first
    print("📖 Scanning documentation...")
    documentation = docs_manager.scan_installed_tools()
    
    print(f"\n📋 Available tools with documentation:")
    for tool_name in documentation.keys():
        overview = docs_manager.get_tool_overview(tool_name)
        status = "✅" if overview.get('has_readme') else "⚠️"
        print(f"  {status} {tool_name}")
    
    print("\n🤖 Ask me anything about your installed tools!")
    print("💡 Examples:")
    print("   - How do I use sd-scripts for training?")
    print("   - What are ComfyUI's main features?")
    print("   - Show me OneTrainer configuration options")
    print("   - Search all docs for 'batch size'")
    print()
    
    while True:
        try:
            question = input("📚 Your question (or 'exit' to quit): ").strip()
            
            if question.lower() in ['exit', 'quit', 'q']:
                break
            
            if not question:
                continue
            
            # Check if it's a search query
            if question.lower().startswith('search'):
                search_term = question.replace('search', '').strip()
                if search_term:
                    results = docs_manager.search_all_documentation(search_term)
                    print(f"\n🔍 Search results for '{search_term}':")
                    for result in results:
                        print(f"  📦 {result['tool_name']} (score: {result['score']})")
                        print(f"     {result['summary'][:200]}...")
                        print()
                continue
            
            # Check if question mentions a specific tool
            mentioned_tool = None
            for tool_name in documentation.keys():
                if tool_name.lower() in question.lower():
                    mentioned_tool = tool_name
                    break
            
            if mentioned_tool:
                answer = docs_manager.query_tool_documentation(mentioned_tool, question)
                print(f"\n📚 {mentioned_tool} Documentation:")
                print(answer)
            else:
                # General question - search across all docs
                print(f"\n🔍 Searching across all documentation...")
                
                # Use Open Interpreter with all available documentation
                all_docs_context = ""
                for tool_name, doc_data in docs_manager.knowledge_base.items():
                    usage = doc_data.get('usage_instructions', '')
                    config_opts = ', '.join(doc_data.get('configuration_options', []))
                    all_docs_context += f"\n{tool_name}: {usage} | Config: {config_opts}\n"
                
                general_prompt = f"""
                Question: {question}
                
                Available AI/ML Tools Documentation:
                {all_docs_context[:5000]}
                
                Please answer the question based on the available documentation.
                If the question is about a specific tool, focus on that tool's documentation.
                """
                
                try:
                    response = interpreter.chat(general_prompt, display=False)
                    if isinstance(response, list) and len(response) > 0:
                        print(response[-1].get('content', 'No response generated'))
                    else:
                        print('No response generated')
                except Exception as e:
                    print(f"❌ Error: {e}")
            
            print("\n" + "-" * 50)
            
        except KeyboardInterrupt:
            break
    
    print("\n📚 Thank you for using Merlin's documentation assistant!")


def model_management_menu():
    """🦙 Model Management Menu"""
    manifest_manager, _ = initialize_merlin()
    
    while True:
        print("\n🦙 Ollama Model Management")
        print("1. Show model status")
        print("2. List available models")
        print("3. Configure default model")
        print("4. Hot-swap model")
        print("5. Model recommendations")
        print("6. Back to main menu")
        
        choice = input("\nChoose option (1-6): ").strip()
        
        if choice == '1':
            manifest_manager.show_model_status()
            
        elif choice == '2':
            models = manifest_manager.list_ollama_models()
            if models:
                print(f"\n📚 Available Ollama Models ({len(models)} total):")
                for model in models:
                    print(f"  🦙 {model.name} ({model.parameter_size}, {model.size_gb}GB)")
                    if model.family != "unknown":
                        print(f"      Family: {model.family}")
            else:
                print("❌ No models found or Ollama not running")
                
        elif choice == '3':
            models = manifest_manager.list_ollama_models()
            if models:
                print("\n🦙 Available models:")
                for i, model in enumerate(models, 1):
                    print(f"{i}. {model.name} ({model.parameter_size}, {model.size_gb}GB)")
                
                try:
                    selection = int(input("\nSelect model number: ")) - 1
                    if 0 <= selection < len(models):
                        model_name = models[selection].name
                        temp = input(f"Temperature (default 0.1): ").strip()
                        temperature = float(temp) if temp else 0.1
                        
                        success = manifest_manager.configure_model(model_name, temperature)
                        if success:
                            print(f"✅ Configured {model_name} as default")
                        else:
                            print(f"❌ Failed to configure {model_name}")
                    else:
                        print("❌ Invalid selection")
                except (ValueError, IndexError):
                    print("❌ Invalid input")
            else:
                print("❌ No models available")
                
        elif choice == '4':
            models = manifest_manager.list_ollama_models()
            if models:
                print("\n🦙 Hot-swap to model:")
                for i, model in enumerate(models, 1):
                    print(f"{i}. {model.name} ({model.parameter_size}, {model.size_gb}GB)")
                
                try:
                    selection = int(input("\nSelect model number: ")) - 1
                    if 0 <= selection < len(models):
                        model_name = models[selection].name
                        temp = input(f"Temperature (press Enter to keep current): ").strip()
                        temperature = float(temp) if temp else None
                        
                        success = manifest_manager.hot_swap_model(model_name, temperature)
                        if success:
                            print(f"🔄 Hot-swapped to {model_name}")
                        else:
                            print(f"❌ Failed to swap to {model_name}")
                    else:
                        print("❌ Invalid selection")
                except (ValueError, IndexError):
                    print("❌ Invalid input")
            else:
                print("❌ No models available")
                
        elif choice == '5':
            recommendations = manifest_manager.get_model_recommendations()
            if recommendations:
                print("\n💡 Model Recommendations by Use Case:")
                for use_case, models in recommendations.items():
                    if models:
                        print(f"\n  {use_case.title()}:")
                        for model in models[:3]:  # Show top 3
                            print(f"    • {model}")
            else:
                print("❌ No recommendations available")
                
        elif choice == '6':
            break
        else:
            print("❌ Invalid choice")


def handle_model_commands(args):
    """Handle model-related command line arguments"""
    manifest_manager, _ = initialize_merlin()
    
    if args.command == 'models':
        models = manifest_manager.list_ollama_models()
        if models:
            print(f"🦙 Available Ollama Models ({len(models)} total):")
            for model in models:
                print(f"  • {model.name} ({model.parameter_size}, {model.size_gb}GB)")
        else:
            print("❌ No models found or Ollama not running")
            
    elif args.command == 'model-status':
        manifest_manager.show_model_status()
        
    elif args.command == 'configure-model':
        if args.model:
            success = manifest_manager.configure_model(args.model, args.temperature)
            if success:
                print(f"✅ Configured {args.model} with temperature {args.temperature}")
            else:
                print(f"❌ Failed to configure {args.model}")
        else:
            print("❌ --model required for configure-model command")
            print("Example: python main.py configure-model --model llama3.1:latest --temperature 0.1")
            
    elif args.command == 'hot-swap':
        if args.model:
            success = manifest_manager.hot_swap_model(args.model, args.temperature if hasattr(args, 'temperature') else None)
            if success:
                print(f"🔄 Hot-swapped to {args.model}")
            else:
                print(f"❌ Failed to swap to {args.model}")
        else:
            print("❌ --model required for hot-swap command")
            print("Example: python main.py hot-swap --model llama3.1:latest")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="🧙‍♂️ Merlin - Simple AMS Assistant")
    parser.add_argument('command', nargs='?', 
                       choices=['status', 'install', 'chat', 'manifests', 'docs', 'scan-docs', 'query', 
                               'models', 'model-status', 'configure-model', 'hot-swap'], 
                       help='Command to run')
    parser.add_argument('--aiml-home', type=str, help='Set AIML_PROJECTS_HOME directory')
    parser.add_argument('--add-repo', type=str, help='Add a GitHub/HuggingFace repository')
    parser.add_argument('--tool', type=str, help='Tool name for documentation queries')
    parser.add_argument('--question', type=str, help='Question to ask about tool documentation')
    parser.add_argument('--model', type=str, help='Model name for configuration or hot-swap')
    parser.add_argument('--temperature', type=float, default=0.1, help='Temperature for model configuration')
    
    args = parser.parse_args()
    
    # Set AIML_PROJECTS_HOME if provided
    if args.aiml_home:
        os.environ['AIML_PROJECTS_HOME'] = args.aiml_home
        print(f"🎯 Set AIML_PROJECTS_HOME to: {args.aiml_home}")
    
    # Handle direct repo addition
    if args.add_repo:
        manifest_manager, modular_installer = initialize_merlin()
        print(f"🔮 Auto-configuring: {args.add_repo}")
        tool_config = manifest_manager.auto_configure_tool(args.add_repo)
        if tool_config:
            result = modular_installer.install_tool(tool_config)
            print(result.message)
        return
    
    if not args.command:
        print_welcome()
        
        while True:
            print("What would you like to do?")
            print("1. Check tool status")
            print("2. Install tools")  
            print("3. Chat with Merlin")
            print("4. Manage manifests")
            print("5. Documentation assistant")
            print("6. Model management")
            print("7. Exit")
            
            choice = input("\n🧙‍♂️ Enter choice (1-7): ").strip()
            
            if choice == '1':
                show_tools_status()
            elif choice == '2':
                selection = select_tools_to_install()
                if selection['type'] != 'invalid':
                    install_tools(selection)
                    print("\n✨ Installation complete!")
            elif choice == '3':
                chat_with_merlin()
            elif choice == '4':
                manage_manifests_menu()
            elif choice == '5':
                docs_interactive_mode()
            elif choice == '6':
                model_management_menu()
            elif choice == '7':
                print("🧙‍♂️ Farewell! May your models converge!")
                break
            else:
                print("❌ Invalid choice")
                
    elif args.command == 'status':
        show_tools_status()
    elif args.command == 'install':
        selection = select_tools_to_install()
        if selection['type'] != 'invalid':
            install_tools(selection)
    elif args.command == 'chat':
        chat_with_merlin()
    elif args.command == 'manifests':
        manage_manifests_menu()
    elif args.command == 'docs':
        docs_interactive_mode()
    elif args.command == 'scan-docs':
        scan_documentation()
    elif args.command == 'query':
        if args.tool and args.question:
            query_tool_docs(args.tool, args.question)
        else:
            print("❌ --tool and --question required for query command")
            print("Example: python main.py query --tool sd-scripts --question 'How do I train a model?'")
    elif args.command in ['models', 'model-status', 'configure-model', 'hot-swap']:
        handle_model_commands(args)


if __name__ == "__main__":
    main()
