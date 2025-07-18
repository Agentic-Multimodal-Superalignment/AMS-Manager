import json
import yaml
import os
import subprocess

class AMSInstaller:
    def __init__(self, manifest_path, config_path="config.yaml", overrides=None):
        self.config = self.load_config(config_path)
        if overrides:
            self.config.update(overrides)
        self.manifest_path = manifest_path
        self.packages = self.load_manifest()
        self.log_file = self.config.get("logging", {}).get("log_file") if self.config.get("logging", {}).get("enabled") else None
        self.verbose = self.config.get("logging", {}).get("verbose", False)

    def load_config(self, config_path):
        try:
            with open(config_path) as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"[Error] Failed to load config: {e}")
            return {}

    def log(self, message):
        if self.log_file:
            try:
                with open(self.log_file, "a") as log:
                    log.write(message + "\n")
            except Exception as e:
                print(f"[Error] Failed to write to log: {e}")
        if self.verbose:
            print(message)

    def load_manifest(self):
        try:
            with open(self.manifest_path) as f:
                data = json.load(f)
            return data.get("packages", [])
        except Exception as e:
            self.log(f"[Error] Failed to load manifest: {e}")
            return []

    def install_package(self, package):
        name = package.get("name")
        url = package.get("url")
        install_cmd = package.get("install", "")
        post_cmd = package.get("post", "")
        dry_run = self.config.get("dry_run", False)
        self.log(f"\n🔧 Installing: {name}")

        try:
            if package["type"] == "github":
                if not os.path.exists(name):
                    cmd = f"git clone {url}"
                    if dry_run:
                        self.log(f"[Dry Run] Would execute: {cmd}")
                    else:
                        subprocess.run(cmd, shell=True)
                        self.log(f"Cloned {name}")
                else:
                    cmd = f"cd {name} && git pull"
                    if dry_run:
                        self.log(f"[Dry Run] Would execute: {cmd}")
                    else:
                        subprocess.run(cmd, shell=True)
                        self.log(f"Updated {name}")
            elif package["type"] == "huggingface":
                cmds = ["git lfs install", f"git clone {url}"]
                for cmd in cmds:
                    if dry_run:
                        self.log(f"[Dry Run] Would execute: {cmd}")
                    else:
                        subprocess.run(cmd, shell=True)
                self.log(f"Cloned HF model {name}")

            if install_cmd:
                if dry_run:
                    self.log(f"[Dry Run] Would execute: {install_cmd}")
                else:
                    subprocess.run(install_cmd, shell=True)
                    self.log(f"Ran install command for {name}")

            if post_cmd:
                if dry_run:
                    self.log(f"[Dry Run] Would execute: {post_cmd}")
                else:
                    subprocess.run(post_cmd, shell=True)
                    self.log(f"Ran post-install command for {name}")

            self.log(f"✅ {name} install step complete.")

        except Exception as e:
            self.log(f"[Error] Failed to install {name}: {e}")

    def install_all(self):
        self.log("📦 Starting AMS Package Installation...\n")
        for pkg in self.packages:
            self.install_package(pkg)

    def summary(self):
        self.log("\n📋 AMS Installer Summary:")
        for pkg in self.packages:
            self.log(f"• {pkg.get('name')} ({pkg.get('type')}) → {pkg.get('url')}")