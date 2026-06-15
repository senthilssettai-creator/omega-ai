import subprocess
from pathlib import Path
from typing import Optional

class PythonSandbox:
    def run(self, script: str, workdir: Optional[str] = None) -> str:
        args = ["python", "-c", script]
        result = subprocess.run(args, cwd=workdir, capture_output=True, text=True)
        return result.stdout.strip() if result.returncode == 0 else result.stderr.strip()
