import time
import uuid
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from app.core.logging import logger
from app.core.exceptions import VoiceBotException, format_error_response


class ProcessingTimeAndSecurityMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id
        start_time = time.time()

        try:
            response = await call_next(request)
            process_time = time.time() - start_time
            response.headers["X-Request-ID"] = request_id
            response.headers["X-Process-Time"] = f"{process_time:.4f}s"
            
            logger.info(
                f"{request.method} {request.url.path} finished in {process_time:.4f}s with status {response.status_code}",
                extra={"request_id": request_id, "processing_time": process_time}
            )
            return response
        except VoiceBotException as exc:
            process_time = time.time() - start_time
            logger.warning(
                f"VoiceBotException: {exc.code} - {exc.message}",
                extra={"request_id": request_id, "processing_time": process_time}
            )
            return JSONResponse(
                status_code=exc.status_code,
                content=format_error_response(exc.code, exc.message, exc.details)
            )
        except Exception as exc:
            process_time = time.time() - start_time
            logger.error(
                f"Unhandled exception during {request.method} {request.url.path}: {str(exc)}",
                exc_info=True,
                extra={"request_id": request_id, "processing_time": process_time}
            )
            return JSONResponse(
                status_code=500,
                content=format_error_response(
                    code="INTERNAL_SERVER_ERROR",
                    message="An unexpected error occurred. Please try again."
                )
            )
