#!/usr/bin/env python3
"""
🧙‍♂️ Documentation Demo - Show how to query documentation without Open Interpreter

This demo shows how the documentation system works even without API keys configured.
"""

import json
from pathlib import Path

def simple_doc_query(aiml_home: str, tool_name: str):
    """Simple documentation query without Open Interpreter"""
    docs_cache = Path(aiml_home) / "docs_cache" / "knowledge_base.json"
    
    if not docs_cache.exists():
        print("❌ No knowledge base found. Run 'scan-docs' first.")
        return
    
    try:
        with open(docs_cache, 'r', encoding='utf-8') as f:
            knowledge_base = json.load(f)
    except Exception as e:
        print(f"❌ Error loading knowledge base: {e}")
        return
    
    if tool_name not in knowledge_base:
        print(f"❌ No documentation found for {tool_name}")
        print(f"Available tools: {', '.join(knowledge_base.keys())}")
        return
    
    tool_docs = knowledge_base[tool_name]
    
    print(f"📚 Documentation for {tool_name}")
    print("=" * 50)
    
    # Show README snippet
    readme_content = tool_docs.get('readme_content', '')
    if readme_content:
        print(f"\n📖 README Preview (first 500 chars):")
        print(readme_content[:500] + "..." if len(readme_content) > 500 else readme_content)
    
    # Show docs files
    docs_files = tool_docs.get('docs_files', [])
    if docs_files:
        print(f"\n📄 Documentation files found ({len(docs_files)}):")
        for doc_file in docs_files[:5]:  # Show first 5
            print(f"   📝 {Path(doc_file).name}")
        if len(docs_files) > 5:
            print(f"   ... and {len(docs_files) - 5} more files")
    
    # Show code examples
    code_examples = tool_docs.get('code_examples', [])
    if code_examples:
        print(f"\n💾 Code examples found ({len(code_examples)}):")
        for i, example in enumerate(code_examples[:3], 1):  # Show first 3
            lines = example.split('\n')
            filename = lines[0] if lines[0].startswith('#') else f"Example {i}"
            print(f"   🐍 {filename}")
            # Show first few lines of code
            code_lines = [line for line in lines[1:10] if line.strip()]
            for line in code_lines[:3]:
                print(f"      {line}")
            if len(code_lines) > 3:
                print(f"      ... ({len(lines)} total lines)")
    
    print(f"\n🔍 Search tip: You can search across all docs with 'search <term>'")
    print(f"🤖 With Open Interpreter configured, you can ask natural language questions!")

def search_all_docs(aiml_home: str, search_term: str):
    """Simple search across all documentation"""
    docs_cache = Path(aiml_home) / "docs_cache" / "knowledge_base.json"
    
    if not docs_cache.exists():
        print("❌ No knowledge base found. Run 'scan-docs' first.")
        return
    
    try:
        with open(docs_cache, 'r', encoding='utf-8') as f:
            knowledge_base = json.load(f)
    except Exception as e:
        print(f"❌ Error loading knowledge base: {e}")
        return
    
    print(f"🔍 Searching for '{search_term}' across all documentation...")
    print("=" * 60)
    
    results = []
    search_lower = search_term.lower()
    
    for tool_name, tool_docs in knowledge_base.items():
        readme_content = tool_docs.get('readme_content', '').lower()
        matches = readme_content.count(search_lower)
        
        if matches > 0:
            # Extract snippet around first match
            index = readme_content.find(search_lower)
            start = max(0, index - 100)
            end = min(len(readme_content), index + 100)
            snippet = tool_docs.get('readme_content', '')[start:end]
            
            results.append({
                'tool': tool_name,
                'matches': matches,
                'snippet': snippet
            })
    
    if not results:
        print(f"❌ No matches found for '{search_term}'")
        return
    
    # Sort by number of matches
    results.sort(key=lambda x: x['matches'], reverse=True)
    
    for result in results[:5]:  # Show top 5 results
        print(f"\n📦 {result['tool']} ({result['matches']} matches)")
        print(f"   {result['snippet'][:200]}...")

if __name__ == "__main__":
    import sys
    
    aiml_home = "M:\\AMS\\ai_projects_folder"  # Set your path here
    
    if len(sys.argv) < 2:
        print("🧙‍♂️ Documentation Demo")
        print("Usage:")
        print("  python doc_demo.py <tool_name>          # Show tool documentation")
        print("  python doc_demo.py search <term>        # Search all documentation")
        print()
        print("Available commands:")
        print("  python doc_demo.py sd-scripts")
        print("  python doc_demo.py OneTrainer")
        print("  python doc_demo.py search 'training'")
        sys.exit(1)
    
    if sys.argv[1] == "search" and len(sys.argv) > 2:
        search_all_docs(aiml_home, sys.argv[2])
    else:
        simple_doc_query(aiml_home, sys.argv[1])
