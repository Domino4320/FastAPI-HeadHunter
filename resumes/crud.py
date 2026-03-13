from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Sequence, delete, update
from core.models.resume import Resume
from resumes.schemas import ResumePostSchema
from sqlalchemy.orm import joinedload
from typing import Any
from core.utils import Specialization


class ResumeProcessor:

    @staticmethod
    async def get_resumes_from_db(session: AsyncSession) -> Sequence[Resume]:
        query = select(Resume).options(joinedload(Resume.worker))
        result = await session.execute(query)
        return result.scalars().all()

    @staticmethod
    async def insert_resume_into_db(
        session: AsyncSession, data: ResumePostSchema
    ) -> None:
        resume = Resume(**data.model_dump())
        session.add(resume)
        await session.commit()

    @staticmethod
    async def delete_resume_from_db(session: AsyncSession, resume_id: int) -> None:
        query = delete(Resume).where(Resume.id == resume_id)
        await session.execute(query)
        await session.commit()

    @staticmethod
    async def patch_resume_into_db(
        session: AsyncSession, resume_id: int, new_data: dict[str, Any]
    ):
        query = update(Resume).values(**new_data).where()
        result = await session.execute(query)
        await session.commit()
        return result.rowcount

    @staticmethod
    async def get_cocrete_resume_from_db(
        session: AsyncSession, resume_id: int
    ) -> Resume:
        result = await session.get(
            Resume, resume_id, options=(joinedload(Resume.worker),)
        )
        return result
