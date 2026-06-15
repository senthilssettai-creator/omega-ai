from typing import List, Optional
from ..config import Settings
from ..openrouter_client import OpenRouterClient

class ExecutorAgent:
    def __init__(self, settings: Settings, client: Optional[OpenRouterClient] = None):
        self.settings = settings
        self.client = client

    def execute(self, plan: str) -> str:
        if self.client and self.settings.openrouter_api_key:
            return self.client.chat(f"Execute with oversight: {plan}", task_type="reasoning")
        return f"Executor running plan:\n{plan}"