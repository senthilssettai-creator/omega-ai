from typing import Optional

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    openrouter_api_key: Optional[str] = None
    database_url: str = "sqlite:///./omega.db"
    playwright_headless: bool = True
    mcp_servers: Optional[str] = None

    model_config = {
        "env_prefix": "",
        "env_file": ".env",
    }
