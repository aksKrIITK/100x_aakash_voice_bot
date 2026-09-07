import edge_tts
from typing import Optional
from app.providers.tts.base import TextToSpeechProvider
from app.core.logging import logger


class EdgeTextToSpeechProvider(TextToSpeechProvider):
    """Free Microsoft Edge Neural TTS Provider with realistic Indian English Male voice."""
    def __init__(self, voice: str = "en-IN-PrabhatNeural"):
        self.voice = voice or "en-IN-PrabhatNeural"  # Realistic Indian English Male Neural Voice

    async def synthesize(self, text: str) -> Optional[bytes]:
        if not text or not text.strip():
            return None

        try:
            communicate = edge_tts.Communicate(text.strip(), self.voice)
            audio_bytes = b""
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    audio_bytes += chunk["data"]

            if audio_bytes:
                return audio_bytes
        except Exception as e:
            logger.warning(f"Edge TTS synthesis failed ({e}). Falling back to browser speech.")

        return None
