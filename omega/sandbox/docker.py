import subprocess
from pathlib import Path
from typing import Optional

class DockerSandbox:
    def run(self, image: str, command: str, workdir: Optional[str] = None) -> str:
        args = ["docker", "run", "--rm"]
        if workdir:
            args += ["-v", f"{Path(workdir).resolve()}:/workspace", "-w", "/workspace"]
        args += [image, "bash", "-lc", command]
        result = subprocess.run(args, capture_output=True, text=True)
        return result.stdout.strip() if result.returncode == 0 else result.stderr.strip()
