from abc import ABC, abstractmethod


class SpeechToTextProvider(ABC):
    @abstractmethod
    async def transcribe(self, audio_bytes: bytes, filename: str = "audio.webm") -> str:
        """Transcribes audio binary data into text."""
        pass
