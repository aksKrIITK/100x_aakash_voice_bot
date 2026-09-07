from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.core.logging import logger
from app.core.middleware import ProcessingTimeAndSecurityMiddleware
from app.db.database import init_db
from app.api.router import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"Starting Aakash AI backend in '{settings.APP_ENV}' environment...")
    await init_db()
    yield
    logger.info("Shutting down Aakash AI backend...")


app = FastAPI(
    title="Aakash AI Voice Bot API",
    description="Conversational AI Voice & Text Interface representing Aakash Kumar",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
origins = settings.CORS_ORIGINS if isinstance(settings.CORS_ORIGINS, list) else [settings.CORS_ORIGINS]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins if origins else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(ProcessingTimeAndSecurityMiddleware)

app.include_router(api_router)


@app.get("/")
async def root():
    return {
        "name": "Aakash AI Voice Bot",
        "tagline": "Talk to an AI that answers as Aakash would.",
        "status": "online",
        "health_check": "/api/v1/health"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=(settings.APP_ENV == "development")
    )
