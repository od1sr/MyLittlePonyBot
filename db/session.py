from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from db.base import Base
import asyncio

DATABASE_URL = "sqlite+aiosqlite:///./test.db"

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = async_sessionmaker(engine, expire_on_commit=False)

# Создание таблиц (один раз)
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
