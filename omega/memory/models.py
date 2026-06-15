from sqlalchemy import Column, String, Integer, Text
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class MemoryEntry(Base):
    __tablename__ = "memory_entries"
    id = Column(Integer, primary_key=True, index=True)
    category = Column(String(50), nullable=False)
    content = Column(Text, nullable=False)
