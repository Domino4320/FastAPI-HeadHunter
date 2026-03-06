from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import URL, create_engine, text
from sqlalchemy.orm import DeclarativeBase
from core.config import settings
from fastapi import APIRouter
from core.models.base import Base
import asyncio


class DatabaseProcessor:

    def __init__(self):
        self.async_engine = create_async_engine(
            url=settings.DATABASE_URL_asyncpg,
            echo=True,
        )
        self.session_factory = async_sessionmaker(
            bind=self.async_engine,
            autoflush=False,  # Действия над объектами переносятся в БД
            autocommit=False,  # Сессия сама фиксирует транзакцию
            expire_on_commit=False,  # Объект пропадает из памяти после commit
        )

    async def create_tables(self):
        async with self.async_engine.connect() as conn:
            # await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)  # CREATE IF NOT EXISTS
            await conn.commit()

    async def get_session(self):
        async with self.session_factory() as session:
            yield session


db_context = DatabaseProcessor()
