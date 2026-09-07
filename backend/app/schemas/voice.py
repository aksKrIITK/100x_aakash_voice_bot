from pydantic import BaseModel


class VoiceChatResponse(BaseModel):
    conversation_id: str
    transcript: str
    answer: str
