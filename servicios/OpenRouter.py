import os
import json
import requests
from typing import Optional

class OpenRouter:
    def __init__(self):
        self.api_key = os.getenv("AI_API_KEY")
        self.base_url = "https://openrouter.ai/api/v1".rstrip("/")
        self.model = "openai/gpt-oss-20b:free"

    def analyze(self, prompt: str) -> Optional[str]:
        max_tokens = 8000
        if not self.api_key:
            return None
        url = f"{self.base_url}/chat/completions"
        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        body = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.3,
            "max_tokens": max_tokens,
        }
        resp = requests.post(url, headers=headers, data=json.dumps(body))
        resp.raise_for_status()
        data = resp.json()
        return data.get("choices", [])[0].get("message", {}).get("content")
