from abc import ABC, abstractmethod
from typing import Optional


class TextToSpeechProvider(ABC):
    @abstractmethod
    async def synthesize(self, text: str) -> Optional[bytes]:
        """Synthesizes text into audio binary data (mp3/wav)."""
        pass
