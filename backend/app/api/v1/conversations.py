from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.conversation import ConversationCreateResponse, ConversationDetailResponse
from app.repositories.conversation_repository import ConversationRepository
from app.dependencies import get_conversation_repository

router = APIRouter()


@router.post("/conversations", response_model=ConversationCreateResponse)
async def create_conversation_endpoint(
    repo: ConversationRepository = Depends(get_conversation_repository)
):
    cid = await repo.create_conversation()
    return ConversationCreateResponse(conversation_id=cid)


@router.get("/conversations/{conversation_id}", response_model=ConversationDetailResponse)
async def get_conversation_endpoint(
    conversation_id: str,
    repo: ConversationRepository = Depends(get_conversation_repository)
):
    conv = await repo.get_conversation(conversation_id)
    if not conv:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Conversation '{conversation_id}' not found."
        )
    return ConversationDetailResponse(**conv)
