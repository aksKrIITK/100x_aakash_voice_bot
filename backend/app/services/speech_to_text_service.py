from app.providers.speech.base import SpeechToTextProvider
from app.providers.speech.openai_provider import OpenAISpeechToTextProvider


class SpeechToTextService:
    def __init__(self, provider: SpeechToTextProvider = None):
        self.provider = provider or OpenAISpeechToTextProvider()

    async def transcribe_audio(self, audio_bytes: bytes, filename: str = "audio.webm") -> str:
        return await self.provider.transcribe(audio_bytes, filename)
