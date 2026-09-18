from fastapi import APIRouter, Response, HTTPException, status
from pydantic import BaseModel, Field
from app.config import settings
from app.providers.tts.edge_provider import EdgeTextToSpeechProvider
from app.providers.tts.elevenlabs_provider import ElevenLabsProvider
from app.providers.tts.openai_provider import OpenAITextToSpeechProvider
from app.core.logging import logger

router = APIRouter()


class TTSRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=4000)
    voice: str = Field(default="en-US-AndrewMultilingualNeural")


@router.post("/tts")
async def tts_endpoint(req: TTSRequest):
    audio_bytes = None

    # 1. ElevenLabs if explicitly configured with API Key and Custom Voice ID
    if getattr(settings, "ELEVENLABS_API_KEY", "") and getattr(settings, "ELEVENLABS_VOICE_ID", ""):
        audio_bytes = await ElevenLabsProvider().synthesize(req.text)

    # 2. Microsoft Edge Neural Multilingual TTS (Andrew / Brian / Prabhat)
    if not audio_bytes:
        voice_to_use = req.voice if req.voice else "en-US-AndrewMultilingualNeural"
        audio_bytes = await EdgeTextToSpeechProvider(voice=voice_to_use).synthesize(req.text)

    # 3. OpenAI TTS fallback if key configured
    if not audio_bytes and getattr(settings, "OPENAI_API_KEY", ""):
        audio_bytes = await OpenAITextToSpeechProvider(voice="echo").synthesize(req.text)

    if not audio_bytes:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Speech synthesis temporarily unavailable."
        )

    return Response(content=audio_bytes, media_type="audio/mpeg")

