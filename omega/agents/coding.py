from typing import Optional

from ..config import Settings
from ..openrouter_client import OpenRouterClient

class CodingAgent:
    def __init__(self, settings: Settings, client: Optional[OpenRouterClient] = None):
        self.settings = settings
        self.client = client

    def develop(self, task: str) -> str:
        if self.client and self.settings.openrouter_api_key:
            return self.client.chat(
                f"Write high-quality Python implementation for the following task:\n{task}",
                task_type="coding",
                max_tokens=450,
            )
        return f"Coding result for '{task}'"

    def review(self, code: str) -> str:
        if self.client and self.settings.openrouter_api_key:
            return self.client.chat(
                f"Review this code for correctness, style, and security:\n{code}",
                task_type="coding",
                max_tokens=300,
            )
        return "Code review unavailable without OpenRouter key."

    def generate_tests(self, description: str) -> str:
        if self.client and self.settings.openrouter_api_key:
            return self.client.chat(
                f"Generate unit tests in Python for this functionality:\n{description}",
                task_type="coding",
                max_tokens=300,
            )
        return "Test generation unavailable without OpenRouter key."
