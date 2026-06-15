from typing import List

from ..config import Settings
from ..memory.manager import MemoryManager

class MemoryAgent:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.storage = MemoryManager(settings=settings)

    def store(self, category: str, content: str) -> None:
        self.storage.store(category, content)

    def recall(self, query: str) -> List[str]:
        return self.storage.search(query)
