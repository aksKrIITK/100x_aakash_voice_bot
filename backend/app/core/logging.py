import logging
import json
import time
from typing import Any, Dict


class JSONFormatter(logging.Formatter):
    """Structured JSON formatter avoiding sensitive secrets in output logs."""

    def format(self, record: logging.LogRecord) -> str:
        log_data: Dict[str, Any] = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "name": record.name,
            "message": record.getMessage(),
        }
        if hasattr(record, "request_id"):
            log_data["request_id"] = getattr(record, "request_id")
        if hasattr(record, "conversation_id"):
            log_data["conversation_id"] = getattr(record, "conversation_id")
        if hasattr(record, "processing_time"):
            log_data["processing_time"] = getattr(record, "processing_time")
        if hasattr(record, "stt_latency"):
            log_data["stt_latency"] = getattr(record, "stt_latency")
        if hasattr(record, "llm_latency"):
            log_data["llm_latency"] = getattr(record, "llm_latency")

        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_data)


def setup_logging():
    logger = logging.getLogger("aakash_ai")
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    handler.setFormatter(JSONFormatter())
    if not logger.handlers:
        logger.addHandler(handler)
    return logger


logger = setup_logging()
