from fastapi import APIRouter
from core.dependencies import SessionDep
from core.enums import WorkFormat, Employment, Experience
from core.filters import FilterCollection, LikeFilter, EqualFilter
from core.models.vacancy import Vacancy
from vacancies.crud import VacancyProcessor
from vacancies.schemas import VacancyGetSchema

router = APIRouter(prefix="/vacancy", tags=["Вакансии"])


@router.get(
    "", summary="Получить все вакансии из БД", response_model=list[VacancyGetSchema]
)
async def get_vacancies(
    session: SessionDep,
    title: str | None = None,
    work_format: WorkFormat | None = None,
    employment: Employment | None = None,
    experience: Experience | None = None,
    employer: str | None = None,
):
    filters = FilterCollection(
        LikeFilter("title", Vacancy, title),
        EqualFilter("work_format", Vacancy, work_format),
        EqualFilter("employment", Vacancy, employment),
        EqualFilter("experience", Vacancy, experience),
        LikeFilter("employer", Vacancy, employer),
    )
    result = await VacancyProcessor.get_vacancies_from_db(
        session, filters.get_full_expression()
    )
    return result
