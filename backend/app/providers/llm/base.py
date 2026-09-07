from abc import ABC, abstractmethod
from typing import List, Dict


class LLMProvider(ABC):
    @abstractmethod
    async def generate(self, messages: List[Dict[str, str]], system_prompt: str = "") -> str:
        """Generates a text completion given message history and optional system prompt."""
        pass
