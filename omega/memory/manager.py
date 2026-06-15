from typing import List

from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

from ..config import Settings
from .models import MemoryEntry

class MemoryManager:
    def __init__(self, settings: Settings):
        self.settings = settings
        database_url = settings.database_url
        if database_url.startswith("sqlite+aiosqlite"):
            database_url = database_url.replace("sqlite+aiosqlite", "sqlite")
        self.engine = create_engine(database_url, future=True)
        self.session_factory = sessionmaker(self.engine, expire_on_commit=False)
        self.initialize()

    def initialize(self) -> None:
        MemoryEntry.metadata.create_all(self.engine)

    def store(self, category: str, content: str) -> None:
        with self.session_factory() as session:
            session.add(MemoryEntry(category=category, content=content))
            session.commit()

    def search(self, query: str) -> List[str]:
        with self.session_factory() as session:
            statement = select(MemoryEntry).where(MemoryEntry.content.ilike(f"%{query}%"))
            results = session.execute(statement).scalars().all()
            return [f"[{entry.category}] {entry.content}" for entry in results]
