from fastapi import APIRouter, Depends
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.conversation_service import ConversationService
from app.dependencies import get_conversation_service

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(
    req: ChatRequest,
    conversation_service: ConversationService = Depends(get_conversation_service)
):
    result = await conversation_service.process_chat(
        conversation_id=req.conversation_id,
        message_text=req.message
    )
    return ChatResponse(**result)
