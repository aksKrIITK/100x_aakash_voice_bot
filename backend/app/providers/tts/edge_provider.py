import re
import edge_tts
from typing import Optional
from app.providers.tts.base import TextToSpeechProvider
from app.core.logging import logger


class EdgeTextToSpeechProvider(TextToSpeechProvider):
    """Microsoft Edge Multilingual Neural TTS Provider for natural human voice delivery."""
    def __init__(self, voice: str = "en-US-AndrewMultilingualNeural"):
        self.voice = voice or "en-US-AndrewMultilingualNeural"

    def _clean_text_for_human_speech(self, text: str) -> str:
        if not text:
            return ""

        cleaned = text.strip()
        # Remove markdown symbols and code backticks
        cleaned = re.sub(r'[*#_`~>[\]()"]', '', cleaned)

        # Technical acronyms normalized for smooth spoken natural pronunciation
        phonetic_map = [
            (r'\bFastAPI\b', 'Fast A P I'),
            (r'\bPostgreSQL\b', 'Postgres Q L'),
            (r'\bIIT\b', 'I I T'),
            (r'\bJNU\b', 'J N U'),
            (r'\bAPI\b', 'A P I'),
            (r'\bAPIs\b', 'A P Is'),
            (r'\bLLM\b', 'L L M'),
            (r'\bLLMs\b', 'L L Ms'),
            (r'\bTTS\b', 'T T S'),
            (r'\bSTT\b', 'S T T'),
            (r'\bB\.?Tech\b', 'B-Tech'),
            (r'\bUI\b', 'U I'),
            (r'\bSaaS\b', 'Sass'),
            (r'\bLangGraph\b', 'Lang Graph'),
            (r'\bLangChain\b', 'Lang Chain'),
            (r'\bGraphQL\b', 'Graph Q L'),
            (r'\bv1\b', 'version 1'),
            (r'\bv3\b', 'version 3'),
        ]
        for pattern, replacement in phonetic_map:
            cleaned = re.sub(pattern, replacement, cleaned, flags=re.IGNORECASE)

        # Natural pauses for dashes and ellipses
        cleaned = re.sub(r'\s*—\s*|\s*--\s*', ', ', cleaned)
        cleaned = re.sub(r'\.{2,}', '... ', cleaned)
        cleaned = re.sub(r'\s+', ' ', cleaned).strip()
        return cleaned

    async def synthesize(self, text: str) -> Optional[bytes]:
        cleaned = self._clean_text_for_human_speech(text)
        if not cleaned:
            return None

        try:
            communicate = edge_tts.Communicate(
                text=cleaned,
                voice=self.voice,
                rate="+0%",
                pitch="+0Hz"
            )
            audio_bytes = b""
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    audio_bytes += chunk["data"]

            if audio_bytes:
                return audio_bytes
        except Exception as e:
            logger.warning(f"Edge TTS synthesis with voice {self.voice} failed ({e}). Falling back to browser speech.")

        return None
