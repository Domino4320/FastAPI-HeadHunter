from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Sequence
from core.models.resume import Resume
from resumes.schemas import ResumePostSchema


class ResumeProcessor:

    @staticmethod
    async def get_resumes_from_db(session: AsyncSession) -> Sequence[Resume]:
        query = select(Resume)
        result = await session.execute(query)
        return result.scalars().all()

    @staticmethod
    async def insert_resume_into_db(
        session: AsyncSession, data: ResumePostSchema
    ) -> None:
        resume = Resume(**data.model_dump())
        session.add(resume)
        await session.commit()
