import httpx
from typing import Optional
from app.config import settings
from app.providers.tts.base import TextToSpeechProvider
from app.core.logging import logger


class ElevenLabsProvider(TextToSpeechProvider):
    """ElevenLabs Cloud TTS Provider for 1:1 Voice Cloning."""
    def __init__(self, api_key: str = "", voice_id: str = ""):
        self.api_key = api_key or getattr(settings, "ELEVENLABS_API_KEY", "")
        self.voice_id = voice_id or getattr(settings, "ELEVENLABS_VOICE_ID", "21m00Tcm4TlvDq8ikWAM")  # Default voice ID

    async def synthesize(self, text: str) -> Optional[bytes]:
        if not self.api_key:
            return None

        url = f"https://api.elevenlabs.io/v1/text-to-speech/{self.voice_id}"
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": self.api_key
        }
        data = {
            "text": text,
            "model_id": "eleven_monolingual_v1",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.75
            }
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=data, headers=headers, timeout=15.0)
                if response.status_code == 200:
                    return response.content
                logger.warning(f"ElevenLabs TTS returned status code {response.status_code}: {response.text}")
        except Exception as e:
            logger.warning(f"ElevenLabs TTS synthesis failed: {e}")

        return None
