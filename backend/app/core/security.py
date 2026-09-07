import os
from typing import Tuple
from app.core.exceptions import AudioValidationError

MAX_AUDIO_SIZE_BYTES = 10 * 1024 * 1024  # 10 MB limit
ALLOWED_MIME_TYPES = {
    "audio/webm",
    "audio/wav",
    "audio/mp3",
    "audio/mpeg",
    "audio/mp4",
    "audio/x-m4a",
    "audio/ogg",
    "audio/aac",
    "application/octet-stream"
}

ALLOWED_EXTENSIONS = {".webm", ".wav", ".mp3", ".m4a", ".ogg", ".mp4", ".aac"}


def validate_audio_file(filename: str, content_type: str, file_size: int) -> Tuple[bool, str]:
    if file_size <= 0:
        raise AudioValidationError("Empty audio recording submitted.")

    if file_size > MAX_AUDIO_SIZE_BYTES:
        raise AudioValidationError("Audio recording exceeds maximum allowed size (10 MB).")

    ext = os.path.splitext(filename)[1].lower()
    
    # Check mime type (ignoring charset or parameters if present)
    base_content_type = content_type.split(";")[0].strip().lower()
    
    if base_content_type not in ALLOWED_MIME_TYPES and ext not in ALLOWED_EXTENSIONS:
        raise AudioValidationError(f"Unsupported audio format '{content_type}'. Allowed formats: webm, wav, mp3, m4a, ogg.")

    return True, "Valid audio file"
