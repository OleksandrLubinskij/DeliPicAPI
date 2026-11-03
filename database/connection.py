from typing import AsyncGenerator

from core.config import db_settings
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

url = db_settings.db_address.get_secret_value()
engine = create_async_engine(url, echo=True)

async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession, 
    expire_on_commit=False
)

async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session