import logging
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from app.config import settings

logger = logging.getLogger("aakash_ai")

Base = declarative_base()

async_engine = None
AsyncSessionLocal = None

if settings.DATABASE_URL:
    db_url = settings.DATABASE_URL
    if db_url.startswith("postgresql://"):
        db_url = db_url.replace("postgresql://", "postgresql+asyncpg://", 1)
    elif db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql+asyncpg://", 1)

    try:
        async_engine = create_async_engine(db_url, echo=False, pool_pre_ping=True)
        AsyncSessionLocal = async_sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession)
        logger.info("Configured PostgreSQL SQLAlchemy database engine.")
    except Exception as e:
        logger.warning(f"Failed to initialize PostgreSQL database engine: {e}. Falling back to in-memory storage.")
else:
    logger.info("DATABASE_URL not configured. Using in-memory conversation storage.")


async def init_db():
    if async_engine:
        try:
            async with async_engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
            logger.info("Database tables initialized successfully.")
        except Exception as e:
            logger.warning(f"Database table initialization failed: {e}. Defaulting to in-memory fallback.")


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    if AsyncSessionLocal:
        async with AsyncSessionLocal() as session:
            try:
                yield session
            except Exception:
                await session.rollback()
                raise
    else:
        yield None
