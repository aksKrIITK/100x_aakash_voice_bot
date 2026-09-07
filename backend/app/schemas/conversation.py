from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional


class MessageSchema(BaseModel):
    id: str
    conversation_id: str
    role: str
    content: str
    created_at: datetime


class ConversationCreateResponse(BaseModel):
    conversation_id: str


class ConversationDetailResponse(BaseModel):
    id: str
    created_at: datetime
    updated_at: datetime
    messages: List[MessageSchema]
