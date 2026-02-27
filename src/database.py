from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import URL, create_engine, text
from sqlalchemy.orm import DeclarativeBase
from src.config import settings
import asyncio

async_engine = create_async_engine(
    url=settings.DATABASE_URL_asyncpg,
    echo=True,
)

async_session_factory = async_sessionmaker(async_engine)

class Base(DeclarativeBase):
    pass