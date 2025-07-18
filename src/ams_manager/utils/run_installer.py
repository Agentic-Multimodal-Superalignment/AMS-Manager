# run_installer.py
from src.ams_manager.core.ams_installer import AMSInstaller

installer = AMSInstaller("ams_manifest.json", "config.yaml")
installer.summary()
installer.install_all()