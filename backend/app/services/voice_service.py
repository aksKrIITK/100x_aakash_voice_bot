import time
from typing import Dict, Any, Optional
from app.services.speech_to_text_service import SpeechToTextService
from app.services.conversation_service import ConversationService
from app.core.security import validate_audio_file
from app.core.exceptions import AudioValidationError, VoiceProcessingError
from app.core.logging import logger


class VoiceService:
    def __init__(
        self,
        conversation_service: ConversationService,
        stt_service: Optional[SpeechToTextService] = None
    ):
        self.conversation_service = conversation_service
        self.stt_service = stt_service or SpeechToTextService()

    async def process_voice_chat(
        self,
        conversation_id: str,
        audio_bytes: bytes,
        filename: str,
        content_type: str,
        provided_transcript: Optional[str] = None
    ) -> Dict[str, Any]:
        start_time = time.time()
        stt_latency = 0.0
        transcript = ""

        if provided_transcript and provided_transcript.strip():
            transcript = provided_transcript.strip()
        else:
            # 1. Validate audio file size & format
            validate_audio_file(filename, content_type, len(audio_bytes))

            # 2. Transcribe audio
            stt_start = time.time()
            try:
                transcript = await self.stt_service.transcribe_audio(audio_bytes, filename)
            except Exception as e:
                logger.error(f"Speech to text transcription failed: {e}")
                raise VoiceProcessingError("We couldn't understand that clearly. Please try again.")

            stt_latency = time.time() - stt_start

        if not transcript or not transcript.strip():
            raise AudioValidationError("No recognizable speech detected in recording.")

        # 3. Dispatch transcript to ConversationService
        response = await self.conversation_service.process_chat(conversation_id, transcript)

        total_time = time.time() - start_time
        logger.info(
            f"Processed voice chat in {total_time:.3f}s (STT latency: {stt_latency:.3f}s)",
            extra={
                "conversation_id": conversation_id,
                "processing_time": total_time,
                "stt_latency": stt_latency
            }
        )

        return {
            "conversation_id": conversation_id,
            "transcript": transcript,
            "answer": response["answer"]
        }
