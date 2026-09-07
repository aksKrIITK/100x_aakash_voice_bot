from typing import Optional
from fastapi import APIRouter, Depends, UploadFile, File, Form
from app.schemas.voice import VoiceChatResponse
from app.services.voice_service import VoiceService
from app.dependencies import get_voice_service
from app.core.exceptions import AudioValidationError

router = APIRouter()


@router.post("/voice/chat", response_model=VoiceChatResponse)
async def voice_chat_endpoint(
    conversation_id: str = Form(...),
    transcript: Optional[str] = Form(None),
    audio: Optional[UploadFile] = File(None),
    voice_service: VoiceService = Depends(get_voice_service)
):
    audio_bytes = b""
    filename = "audio.webm"
    content_type = "audio/webm"

    if audio:
        audio_bytes = await audio.read()
        filename = audio.filename or "audio.webm"
        content_type = audio.content_type or "audio/webm"

    result = await voice_service.process_voice_chat(
        conversation_id=conversation_id,
        audio_bytes=audio_bytes,
        filename=filename,
        content_type=content_type,
        provided_transcript=transcript
    )
    return VoiceChatResponse(**result)
