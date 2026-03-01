from sqlalchemy import text, insert, values, select, delete, update, Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from .schemas import WorkerPostSchema, WorkerPatchSchema
from core.models.worker import Worker
from typing import Any
from core.database import db_context, Base


class WorkersProcessor:

    @staticmethod
    async def insert_worker_into_db(
        data: WorkerPostSchema, session: AsyncSession
    ) -> None:
        worker = Worker(**data.model_dump())
        session.add(worker)
        await session.commit()

    @staticmethod
    async def get_workers_from_db(session: AsyncSession) -> Sequence[Worker]:
        query = select(Worker)
        result = await session.execute(query)
        return result.scalars().all()

    @staticmethod
    async def delete_worker_from_db(id: int, session: AsyncSession) -> None:
        query = delete(Worker).where(Worker.id == id)
        await session.execute(query)
        await session.commit()

    @staticmethod
    async def patch_worker_from_db(
        id: int, new_data: dict[str, Any], session: AsyncSession
    ) -> int:
        query = update(Worker).values(**new_data).where(Worker.id == id)
        result = await session.execute(query)
        await session.commit()
        return result.rowcount

    @staticmethod
    async def get_concrete_worker(worker_id: int, session: AsyncSession) -> Worker:
        return await session.get(Worker, worker_id)
