from typing import Optional
import requests

from ..config import Settings
from ..openrouter_client import OpenRouterClient

class ResearchAgent:
    def __init__(self, settings: Settings, client: Optional[OpenRouterClient] = None):
        self.settings = settings
        self.client = client

    def investigate(self, query: str) -> str:
        if self.client and self.settings.openrouter_api_key:
            return self.client.chat(
                f"Analyze and summarize the most relevant information for this research topic:\n{query}",
                task_type="research",
                max_tokens=400,
            )
        return f"Research summary for '{query}'"

    def search_web(self, url: str) -> str:
        try:
            response = requests.get(url, timeout=15)
            response.raise_for_status()
            snippet = response.text[:1200].replace("\n", " ")
            if self.client and self.settings.openrouter_api_key:
                return self.client.chat(
                    f"Summarize this page content from {url}:\n{snippet}",
                    task_type="research",
                    max_tokens=300,
                )
            return snippet
        except requests.RequestException as exc:
            return f"Web search failed for {url}: {exc}"
