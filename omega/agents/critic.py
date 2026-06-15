from ..config import Settings

class CriticAgent:
    def __init__(self, settings: Settings):
        self.settings = settings

    def review(self, output: str) -> str:
        return f"Critic analysis for '{output}'"