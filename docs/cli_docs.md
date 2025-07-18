# AMS Installer CLI Docs

### 1. Connect Open interpreter to ollama

```
interpreter --api_base http://localhost:11434 --api_key fake_key --model my-custom-model
```

For in python code use the following:

```
from interpreter import interpreter

interpreter.offline = True
interpreter.llm.model = "my-custom-model"
interpreter.llm.api_key = "fake_key"
interpreter.llm.api_base = "http://localhost:11434"

interpreter.chat()
```

To inspect open interpreter behavior use the following:

```
interpreter --verbose
```

### 🧬 Bonus Integration: AMSInstaller + Open Interprete

You can wrap your whole install operation inside an interactive command, like:

```
interpreter.chat("Run AMSInstaller with manifest 'ams_manifest.json' and profile 'experimental'")
```

Or you embed the call directly:

```
interpreter.computer.run(
    "python",
    "from ams_installer import AMSInstaller\n"
    "installer = AMSInstaller('ams_manifest.json', 'config.yaml')\n"
    "installer.install_all()"
)
```

And then say:

“Please verify which packages installed correctly.”

Open Interpreter will stream the output as if Merlin herself were reading the scroll aloud.