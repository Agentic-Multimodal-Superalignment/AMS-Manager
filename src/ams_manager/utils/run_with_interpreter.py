# run_with_interpreter.py
from interpreter import interpreter

interpreter.computer.run(
    "python",
    "from ams_installer import AMSInstaller\n"
    "installer = AMSInstaller('ams_manifest.json')\n"
    "installer.install_all()"
)