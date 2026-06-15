from typing import List, Optional
from ..config import Settings
from ..openrouter_client import OpenRouterClient

class PlannerAgent:
    def __init__(self, settings: Settings, client: Optional[OpenRouterClient] = None):
        self.settings = settings
        self.client = client

    def create_plan(self, goal: str) -> str:
        if self.client and self.settings.openrouter_api_key:
            prompt = f"Create a structured task plan for the goal: {goal}"
            return self.client.chat(prompt, task_type="planning")

        tasks: List[str] = [
            f"Analyze goal: {goal}",
            "Generate task breakdown",
            "Assign work to agents",
            "Return structured plan"
        ]
        return "\n".join(tasks)
