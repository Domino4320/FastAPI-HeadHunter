from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import URL, create_engine, text
from sqlalchemy.orm import DeclarativeBase
from config import settings
from fastapi import APIRouter
import asyncio

async_engine = create_async_engine(
    url=settings.DATABASE_URL_asyncpg,
    echo=True,
)

async_session_factory = async_sessionmaker(async_engine)

class Base(DeclarativeBase):
    pass   

class DatabaseProcessor:

    @staticmethod
    async def create_tables():
        async with async_engine.connect() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
            await conn.commit()

router = APIRouter(prefix="/database", tags=["БД"])

@router.get("/")
async def create_database():
    await DatabaseProcessor.create_tables()
    return {"success" : True}
