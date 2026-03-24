from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import BinaryExpression, select
from sqlalchemy.orm import selectinload
from core.models.vacancy import Vacancy


class VacancyProcessor:

    @staticmethod
    async def get_vacancies_from_db(
        session: AsyncSession, filters: BinaryExpression
    ) -> list[Vacancy]:
        query = select(Vacancy).where(filters)
        result = await session.execute(query)
        return list(result.scalars().all())

    @staticmethod
    async def get_vacancies_with_responses_from_db(
        session: AsyncSession, filters: BinaryExpression
    ) -> list[Vacancy]:
        query = (
            select(Vacancy)
            .where(filters)
            .options(selectinload(Vacancy.vacancy_responses))
        )
        result = await session.execute(query)
        return list(result.scalars().all())
