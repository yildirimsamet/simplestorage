import asyncio
import logging
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from app.core.config import settings

logger = logging.getLogger(__name__)


class Base(DeclarativeBase):
    pass


engine = create_async_engine(settings.database_url, echo=True)
async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_async_session() -> AsyncSession:
    async with async_session_maker() as session:
        yield session


async def create_tables():
    max_retries = 30
    retry_delay = 1

    for attempt in range(max_retries):
        try:
            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
            logger.info("Database tables created successfully")
            return
        except Exception as e:
            if attempt == max_retries - 1:
                logger.error(f"Failed to create tables after {max_retries} attempts: {e}")
                raise

            logger.warning(f"Attempt {attempt + 1} failed, retrying in {retry_delay}s: {e}")
            await asyncio.sleep(retry_delay)