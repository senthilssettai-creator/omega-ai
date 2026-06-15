import subprocess
from typing import Optional

from ..config import Settings

class DevOpsAgent:
    def __init__(self, settings: Settings):
        self.settings = settings

    def deploy(self, target: str) -> str:
        return f"Deploying '{target}'"

    def git_status(self) -> str:
        result = subprocess.run(["git", "status", "--short"], capture_output=True, text=True)
        return result.stdout.strip() or "Clean working tree."

    def git_commit(self, message: str) -> str:
        add = subprocess.run(["git", "add", "-A"], capture_output=True, text=True)
        if add.returncode != 0:
            return add.stderr.strip()
        commit = subprocess.run(["git", "commit", "-m", message], capture_output=True, text=True)
        return commit.stdout.strip() if commit.returncode == 0 else commit.stderr.strip()

    def docker_build(self, tag: str, dockerfile: str = "Dockerfile") -> str:
        result = subprocess.run(["docker", "build", "-t", tag, "-f", dockerfile, "."], capture_output=True, text=True)
        return result.stdout.strip() if result.returncode == 0 else result.stderr.strip()

    def shell(self, command: str) -> str:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.stdout.strip() if result.returncode == 0 else result.stderr.strip()
