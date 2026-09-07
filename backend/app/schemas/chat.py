from pydantic import BaseModel, Field
from typing import Optional


class ChatRequest(BaseModel):
    conversation_id: str = Field(..., description="UUID identifying the conversation session")
    message: str = Field(..., min_length=1, max_length=2000, description="User question or text prompt")


class ChatResponse(BaseModel):
    conversation_id: str
    answer: str
