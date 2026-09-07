from typing import List, Dict
from app.providers.llm.base import LLMProvider
from app.providers.llm.openai_provider import OpenAIProvider


class LLMService:
    def __init__(self, provider: LLMProvider = None):
        self.provider = provider or OpenAIProvider()

    async def generate_response(self, messages: List[Dict[str, str]], system_prompt: str) -> str:
        return await self.provider.generate(messages, system_prompt)
