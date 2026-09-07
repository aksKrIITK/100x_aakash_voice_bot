from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from typing import Optional, Dict, Any


class VoiceBotException(Exception):
    """Base application exception."""
    def __init__(self, code: str, message: str, status_code: int = status.HTTP_400_BAD_REQUEST, details: Optional[Dict[str, Any]] = None):
        self.code = code
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)


class AudioValidationError(VoiceBotException):
    def __init__(self, message: str = "Invalid audio file format or size limit exceeded."):
        super().__init__(
            code="AUDIO_VALIDATION_ERROR",
            message=message,
            status_code=status.HTTP_400_BAD_REQUEST
        )


class VoiceProcessingError(VoiceBotException):
    def __init__(self, message: str = "We couldn't process your voice. Please try again."):
        super().__init__(
            code="VOICE_PROCESSING_FAILED",
            message=message,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


class ConversationNotFoundError(VoiceBotException):
    def __init__(self, conversation_id: str):
        super().__init__(
            code="CONVERSATION_NOT_FOUND",
            message=f"Conversation {conversation_id} was not found.",
            status_code=status.HTTP_404_NOT_FOUND
        )


class ProviderError(VoiceBotException):
    def __init__(self, message: str = "AI service temporarily unavailable. Please try again."):
        super().__init__(
            code="PROVIDER_ERROR",
            message=message,
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE
        )


def format_error_response(code: str, message: str, details: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    res = {
        "error": {
            "code": code,
            "message": message
        }
    }
    if details:
        res["error"]["details"] = details
    return res
