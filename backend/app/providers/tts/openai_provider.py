from typing import Optional
from app.config import settings
from app.providers.tts.base import TextToSpeechProvider
from app.core.logging import logger


class OpenAITextToSpeechProvider(TextToSpeechProvider):
    """OpenAI Cloud TTS Provider (using male voice echo/onyx/fable)."""
    def __init__(self, api_key: str = "", voice: str = "echo"):
        self.api_key = api_key or settings.OPENAI_API_KEY
        self.voice = voice or "echo"  # "echo", "onyx", or "fable" are realistic male voices
        self.client = None
        if self.api_key:
            try:
                import openai
                self.client = openai.AsyncOpenAI(api_key=self.api_key)
            except Exception as e:
                logger.warning(f"Failed to initialize OpenAI TTS Client: {e}")

    async def synthesize(self, text: str) -> Optional[bytes]:
        if not self.client:
            return None

        try:
            response = await self.client.audio.speech.create(
                model="tts-1",
                voice=self.voice,
                input=text
            )
            return response.content
        except Exception as e:
            logger.warning(f"OpenAI TTS synthesis failed: {e}")

        return None
