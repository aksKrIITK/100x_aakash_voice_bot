from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db_session
from app.repositories.conversation_repository import ConversationRepository
from app.services.conversation_service import ConversationService
from app.services.voice_service import VoiceService
from app.services.llm_service import LLMService
from app.services.speech_to_text_service import SpeechToTextService


def get_conversation_repository(session: AsyncSession = Depends(get_db_session)) -> ConversationRepository:
    return ConversationRepository(session=session)


def get_conversation_service(
    repo: ConversationRepository = Depends(get_conversation_repository)
) -> ConversationService:
    return ConversationService(repository=repo, llm_service=LLMService())


def get_voice_service(
    conv_service: ConversationService = Depends(get_conversation_service)
) -> VoiceService:
    return VoiceService(conversation_service=conv_service, stt_service=SpeechToTextService())
