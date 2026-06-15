from pathlib import Path
from typing import List

class FilesystemPlugin:
    def read(self, path: str) -> str:
        return Path(path).read_text()

    def write(self, path: str, content: str) -> None:
        Path(path).write_text(content)

    def delete(self, path: str) -> None:
        Path(path).unlink(missing_ok=True)

    def move(self, source: str, destination: str) -> None:
        Path(source).replace(destination)

    def search(self, directory: str, pattern: str = "*") -> List[str]:
        return [str(p) for p in Path(directory).rglob(pattern)]