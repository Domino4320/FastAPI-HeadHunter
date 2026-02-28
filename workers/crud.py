from sqlalchemy import text, insert, values, select, delete, update
from database import async_engine, async_session_factory, Base
from sqlalchemy.ext.asyncio import AsyncSession
from .schemas import WorkerPostSchema, WorkerPatchSchema
from models import workers_table, WorkersOrm, ResumesOrm
from typing import Any

class WorkersProcessor:

    @staticmethod
    async def insert_worker_into_db(data : WorkerPostSchema):
        worker = WorkersOrm(**data.model_dump())
        async with async_session_factory() as session:
            session.add(worker)
            await session.commit()

    @staticmethod
    async def get_workers_from_db():
        async with async_session_factory() as session:
            query = select(WorkersOrm)
            result = await session.execute(query)
        return result.scalars().all()
    
    @staticmethod 
    async def delete_worker_from_db(id : int):
        async with async_session_factory() as session:
            query = delete(WorkersOrm).where(WorkersOrm.id == id)
            await session.execute(query)
            await session.commit()

    @staticmethod
    async def patch_worker_from_db(id : int, new_data : dict[str, Any]):
        async with async_session_factory() as session:
            query = update(WorkersOrm).values(**new_data).where(WorkersOrm.id == id)
            result = await session.execute(query)
            await session.commit()
        return result.rowcount


