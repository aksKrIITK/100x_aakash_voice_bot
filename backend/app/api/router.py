from fastapi import APIRouter
from app.api.v1 import health, chat, voice, conversations, tts

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(health.router, tags=["Health"])
api_router.include_router(conversations.router, tags=["Conversations"])
api_router.include_router(chat.router, tags=["Chat"])
api_router.include_router(voice.router, tags=["Voice"])
api_router.include_router(tts.router, tags=["TTS"])
