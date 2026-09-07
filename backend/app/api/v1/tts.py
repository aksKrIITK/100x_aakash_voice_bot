from fastapi import APIRouter, Response, HTTPException, status
from pydantic import BaseModel, Field
from app.providers.tts.edge_provider import EdgeTextToSpeechProvider
from app.providers.tts.elevenlabs_provider import ElevenLabsProvider
from app.providers.tts.openai_provider import OpenAITextToSpeechProvider

router = APIRouter()


class TTSRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=4000)
    voice: str = Field(default="en-IN-PrabhatNeural")  # Options: en-IN-PrabhatNeural, en-US-GuyNeural, en-IN-NeerjaNeural


@router.post("/tts")
async def tts_endpoint(req: TTSRequest):
    # Try ElevenLabs if configured, else OpenAI if configured, else free Edge Neural TTS (en-IN-PrabhatNeural)
    audio_bytes = await ElevenLabsProvider().synthesize(req.text)
    
    if not audio_bytes:
        audio_bytes = await OpenAITextToSpeechProvider().synthesize(req.text)

    if not audio_bytes:
        audio_bytes = await EdgeTextToSpeechProvider(voice=req.voice).synthesize(req.text)

    if not audio_bytes:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Speech synthesis temporarily unavailable."
        )

    return Response(content=audio_bytes, media_type="audio/mpeg")
