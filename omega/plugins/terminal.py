import subprocess
from typing import List

class TerminalPlugin:
    def run(self, command: str) -> str:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.stdout.strip() if result.returncode == 0 else result.stderr.strip()

    def history(self, count: int = 20) -> List[str]:
        return []
