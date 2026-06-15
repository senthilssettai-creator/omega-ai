import json
import os
import requests
from typing import Optional

from .config import Settings

class ModelRouter:
    TASK_MODEL_MAP = {
        "reasoning": ["deepseek-mini", "qwen-v1", "kiki-3b"],
        "coding": ["deepseek-coder", "qwen-coder"],
        "research": ["deepseek-mini", "kiki-3b"],
        "planning": ["qwen-v1", "deepseek-mini"],
        "fast": ["gemma", "llama-3"],
        "long_context": ["kiki-16k", "qwen-long"],
    }

    def choose_model(self, task_type: str = "reasoning") -> str:
        candidates = self.TASK_MODEL_MAP.get(task_type.lower(), self.TASK_MODEL_MAP["reasoning"])
        return candidates[0]

class OpenRouterClient:
    BASE_URL = "https://api.openrouter.ai/v1"

    def __init__(self, settings: Settings):
        self.key = settings.openrouter_api_key
        self.router = ModelRouter()

    def _headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self.key}",
            "Content-Type": "application/json",
        }

    def chat(self, prompt: str, task_type: str = "reasoning", max_tokens: int = 500) -> str:
        if not self.key:
            return f"[fallback] {task_type} output for: {prompt}"
        model = self.router.choose_model(task_type)
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens,
        }
        response = requests.post(f"{self.BASE_URL}/chat/completions", json=payload, headers=self._headers(), timeout=60)
        response.raise_for_status()
        data = response.json()
        choice = data.get("choices", [{}])[0]
        message = choice.get("message", {}).get("content")
        if message is None:
            raise RuntimeError("OpenRouter returned an unexpected response")
        return message.strip()

    def embed(self, text: str) -> list[float]:
        if not self.key:
            return []
        model = self.router.choose_model("reasoning")
        payload = {
            "model": model,
            "input": text,
        }
        response = requests.post(f"{self.BASE_URL}/embeddings", json=payload, headers=self._headers(), timeout=60)
        response.raise_for_status()
        data = response.json()
        embedding = data.get("data", [{}])[0].get("embedding")
        if embedding is None:
            raise RuntimeError("OpenRouter embedding failed")
        return embedding