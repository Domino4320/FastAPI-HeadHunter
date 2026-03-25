from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import BinaryExpression, select, delete
from sqlalchemy.orm import selectinload
from core.models.vacancy import Vacancy
from vacancies.schemas import VacancyPostSchema


class VacancyProcessor:

    @staticmethod
    async def get_vacancies_from_db(
        session: AsyncSession,
        filters: BinaryExpression,
        with_responses: bool,
    ) -> list[Vacancy]:
        query = (
            (
                select(Vacancy)
                .where(filters)
                .options(selectinload(Vacancy.vacancy_responses))
            )
            if with_responses
            else select(Vacancy).where(filters)
        )
        result = await session.execute(query)
        return list(result.scalars().all())

    @staticmethod
    async def get_vacancy_by_id_from_db(
        session: AsyncSession,
        vacancy_id: int,
        with_responses: bool,
    ) -> Vacancy | None:
        result = (
            await session.get(Vacancy, vacancy_id)
            if with_responses
            else await session.get(
                Vacancy, vacancy_id, options=selectinload(Vacancy.vacancy_responses)
            )
        )
        return result

    @staticmethod
    async def insert_vacancy_into_db(
        session: AsyncSession,
        data: VacancyPostSchema,
    ) -> None:
        new_vacancy = Vacancy(**data.model_dump())
        session.add(new_vacancy)
        await session.commit()

    @staticmethod
    async def delete_vacancy_from_db(
        session: AsyncSession,
        vacancy_id: int,
    ) -> None:
        query = delete(Vacancy).where(Vacancy.id == vacancy_id)
        await session.execute(query)
        await session.commit()
