from fastapi import APIRouter, Path
from core.dependencies import SessionDep
from core.enums import WorkFormat, Employment, Experience
from core.filters import FilterCollection, LikeFilter, EqualFilter
from core.models.vacancy import Vacancy
from vacancies.crud import VacancyProcessor
from vacancies.schemas import VacancyGetSchema, VacancyPostSchema

router = APIRouter(prefix="/vacancy", tags=["Вакансии"])


@router.get("", summary="Получить все вакансии из БД")
async def get_vacancies(
    session: SessionDep,
    title: str | None = None,
    work_format: WorkFormat | None = None,
    employment: Employment | None = None,
    experience: Experience | None = None,
    employer: str | None = None,
    with_responses: bool = False,
):
    filters = FilterCollection(
        LikeFilter("title", Vacancy, title),
        EqualFilter("work_format", Vacancy, work_format),
        EqualFilter("employment", Vacancy, employment),
        EqualFilter("experience", Vacancy, experience),
        LikeFilter("employer", Vacancy, employer),
    )
    result = await VacancyProcessor.get_vacancies_from_db(
        session,
        filters.get_full_expression(),
        with_responses,
    )
    return result if result else {"message": "not found"}


@router.get("/{vacancy_id}", summary="Получить вакансию по id из БД")
async def get_vacancy_by_id(
    session: SessionDep, vacancy_id: int = Path(ge=1), with_responses: bool = False
):
    result = VacancyProcessor.get_vacancy_by_id_from_db(
        session,
        vacancy_id,
        with_responses,
    )
    return result if result else {"message": "not found"}


@router.post("/", summary="Добавить вакансию в БД")
async def add_vacancy(session: SessionDep, data: VacancyPostSchema):
    await VacancyProcessor.insert_vacancy_into_db(session, data)
    return {"success": True}


@router.delete("/{vacancy_id}", summary="Удалить вакансию из БД")
async def delete_vacancy(
    session: SessionDep,
    vacancy_id: int,
):
    await VacancyProcessor.delete_vacancy_from_db(session, vacancy_id)
    return {"success": True}
