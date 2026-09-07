import io
import asyncio
from app.config import settings
from app.providers.speech.base import SpeechToTextProvider
from app.core.logging import logger


class MockSpeechToTextProvider(SpeechToTextProvider):
    """Fallback STT provider that cycles sample interview questions when no STT API key is provided."""
    _index = 0
    _questions = [
        "Tell me about your life story and journey",
        "What is your #1 superpower?",
        "What are the top 3 areas you want to grow in?",
        "What misconception do your coworkers have about you?",
        "How do you push your boundaries and limits?",
        "What motivates you to build software?"
    ]

    async def transcribe(self, audio_bytes: bytes, filename: str = "audio.webm") -> str:
        await asyncio.sleep(0.4)
        q = MockSpeechToTextProvider._questions[MockSpeechToTextProvider._index % len(MockSpeechToTextProvider._questions)]
        MockSpeechToTextProvider._index += 1
        return q


class OpenAISpeechToTextProvider(SpeechToTextProvider):
    def __init__(self, api_key: str = ""):
        self.fallback = MockSpeechToTextProvider()
        self.client = None
        
        groq_key = settings.GROQ_API_KEY or (api_key if settings.STT_PROVIDER == "groq" else "")
        openai_key = api_key or settings.OPENAI_API_KEY

        if groq_key:
            self.api_key = groq_key
            self.model = settings.GROQ_STT_MODEL or "whisper-large-v3"
            try:
                import openai
                self.client = openai.AsyncOpenAI(api_key=self.api_key, base_url="https://api.groq.com/openai/v1")
                logger.info(f"Initialized Groq Whisper STT Client with model {self.model}")
            except Exception as e:
                logger.warning(f"Failed to initialize Groq Whisper Client: {e}. Will use fallback STT.")
        elif openai_key:
            self.api_key = openai_key
            self.model = "whisper-1"
            try:
                import openai
                self.client = openai.AsyncOpenAI(api_key=self.api_key)
                logger.info("Initialized OpenAI Whisper STT Client")
            except Exception as e:
                logger.warning(f"Failed to initialize OpenAI Whisper Client: {e}. Will use fallback STT.")

    async def transcribe(self, audio_bytes: bytes, filename: str = "audio.webm") -> str:
        if not self.client:
            return await self.fallback.transcribe(audio_bytes, filename)

        try:
            audio_file = io.BytesIO(audio_bytes)
            audio_file.name = filename
            
            transcript_obj = await self.client.audio.transcriptions.create(
                model=self.model,
                file=audio_file
            )
            return transcript_obj.text.strip()
        except Exception as e:
            logger.warning(f"Whisper STT call failed ({e}). Falling back to local STT mock.")
            return await self.fallback.transcribe(audio_bytes, filename)
