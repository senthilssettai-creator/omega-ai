from __future__ import annotations
from typing import Dict

from ..config import Settings

class MCPManager:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.servers: Dict[str, str] = {}
        self.discover_from_env()

    def discover_from_env(self) -> None:
        raw = self.settings.mcp_servers or ""
        for token in raw.split(","):
            token = token.strip()
            if not token:
                continue
            if "=" in token:
                name, url = token.split("=", 1)
                self.servers[name.strip()] = url.strip()
            else:
                self.servers[f"server_{len(self.servers) + 1}"] = token

    def register(self, name: str, url: str) -> None:
        self.servers[name] = url

    def list_servers(self) -> Dict[str, str]:
        return dict(self.servers)