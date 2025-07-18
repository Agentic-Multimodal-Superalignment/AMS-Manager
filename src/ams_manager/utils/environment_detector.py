#!/usr/bin/env python3
"""
🔍 Simple Environment Detector for Merlin

Just the basics - no complex scanning, just AIML_PROJECTS_HOME directory checking.
"""

import os
import sys
import platform
from pathlib import Path
from typing import Dict, List
from dataclasses import dataclass


@dataclass
class SimpleSystemInfo:
    """Basic system information"""
    system: str
    python_version: str
    python_path: str
    git_available: bool
    aiml_home: str


class SimpleEnvironmentDetector:
    """🧙‍♂️ Simple Environment Detector - Keep it magical, keep it simple!"""
    
    def __init__(self):
        self.aiml_home = self.get_aiml_home()
    
    def get_aiml_home(self) -> Path:
        """Get AIML_PROJECTS_HOME directory"""
        home_dir = os.environ.get('AIML_PROJECTS_HOME')
        if home_dir:
            return Path(home_dir)
        return Path.home() / 'aiml_projects'
    
    def get_system_info(self) -> SimpleSystemInfo:
        """Get basic system information"""
        return SimpleSystemInfo(
            system=platform.system(),
            python_version=sys.version.split()[0],
            python_path=sys.executable,
            git_available=self._check_git_available(),
            aiml_home=str(self.aiml_home)
        )
    
    def _check_git_available(self) -> bool:
        """Check if Git is available"""
        try:
            import subprocess
            subprocess.run(['git', '--version'], capture_output=True, check=True)
            return True
        except:
            return False
    
    def scan_for_ai_tools(self) -> Dict[str, Dict]:
        """Scan AIML_PROJECTS_HOME for installed tools"""
        if not self.aiml_home.exists():
            return {}
        
        tools = {}
        
        # Simple directory checks
        tools['comfyui'] = {
            'found': (self.aiml_home / 'ComfyUI').exists(),
            'locations': [str(self.aiml_home / 'ComfyUI')] if (self.aiml_home / 'ComfyUI').exists() else []
        }
        tools['fluxgym'] = {
            'found': (self.aiml_home / 'fluxgym').exists(),
            'locations': [str(self.aiml_home / 'fluxgym')] if (self.aiml_home / 'fluxgym').exists() else []
        }
        tools['onetrainer'] = {
            'found': (self.aiml_home / 'OneTrainer').exists(),
            'locations': [str(self.aiml_home / 'OneTrainer')] if (self.aiml_home / 'OneTrainer').exists() else []
        }
        
        # For open-webui, check if command is available (it's a pip package)
        try:
            import subprocess
            subprocess.run(['open-webui', '--version'], capture_output=True)
            tools['open-webui'] = {'found': True, 'locations': ['system-wide']}
        except:
            tools['open-webui'] = {'found': False, 'locations': []}
        
        return tools
