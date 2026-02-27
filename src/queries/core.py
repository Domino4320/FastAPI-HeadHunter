from sqlalchemy import text, insert, values, select, delete, update
from src.database import async_engine, async_session_factory, Base
from sqlalchemy.ext.asyncio import AsyncSession
from src.schemas import WorkerPostSchema, WorkerPatchSchema
from src.models import workers_table, WorkersOrm, ResumesOrm
from typing import Any

class DatabaseProcessor:

    @staticmethod
    async def create_tables():
        async with async_engine.connect() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
            await conn.commit()

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





















# def insert_worker_into_db(data : WorkerPostSchema):
#     worker = WorkersOrm(
#         username = data.username
#     )
#     with session_factory() as session:
#         session.add(worker)        
#         session.commit()

# def get_workers_from_db():
#     with session_factory() as session:
#         result = session.get(WorkersOrm)
#     return [dict(row) for row in result.mappings()]

# def insert_resume_into_db(data : ResumePostSchema):
#     resume = ResumesOrm(
#         title = data.title,
#         salary = data.salary,
#         workload = data.workload,
#         worker_id = data.worker_id
#     )
#     with session_factory() as session:
#         session.add(resume)
#         session.commit()

# def get_resumes_from_db():
#     with session_factory() as session:
#         result = session.get(ResumesOrm)
#     return [dict(row) for row in result.mappings()]

