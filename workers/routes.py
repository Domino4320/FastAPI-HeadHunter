from fastapi import APIRouter, HTTPException, status, Path, Query
from .crud import WorkersProcessor
from core.dependencies import SessionDep, AdminRequieredDep
from core.models import Worker
from workers.schemas import (
    WorkerGetSchemaWithResume,
    WorkerPatchSchema,
    WorkerPostSchema,
    WorkerGetSchema,
)
from resumes.schemas import ResumeGetSchema  # положил класс в globals
from typing import Annotated, List
from core.enums import Specialization, City, Status
from core.utils import ResultCheck
from core.query_schemas import PositiveRangeValuesSchema
from core.filters import LikeFilter, EqualFilter, RangeFilter, FilterCollection

WorkerGetSchemaWithResume.model_rebuild()  # заребилдил модель, чтобы строковая аннотация превратилась в класс

router = APIRouter(prefix="/workers", tags=["Работники"])
WorkerID = Annotated[int, Path(gt=0)]
# Annotated перегружает магический метод __class_getitem__ в котором создает
# объект в который записывает тип как 1 атрибут объекта, а все остальные метаданные как другой


@router.get(
    "/",
    response_model=List[WorkerGetSchemaWithResume],
    summary="Получить всех работников из БД",
)
async def get_workers(
    session: SessionDep,
    age_range: Annotated[
        PositiveRangeValuesSchema, Query(description="age range of workers")
    ] = None,
    specialization: Specialization | None = None,
    city: City | None = None,
    status: Status | None = None,
):
    filters = FilterCollection(
        RangeFilter("age", Worker, age_range),
        EqualFilter("specialization", Worker, specialization),
        EqualFilter("city", Worker, city),
        EqualFilter("status", Worker, status),
    )
    result = await WorkersProcessor.get_workers_from_db(
        session, filters.get_full_expression()
    )
    ResultCheck.check_result(result, "workers wasn`t found")
    return result


@router.post("/", summary="Отправить работника в БД")
async def post_worker(data: WorkerPostSchema, session: SessionDep):
    await WorkersProcessor.insert_worker_into_db(data, session)
    return {"success": True}


@router.delete("/{worker_id}", summary="Удалить работника из БД")
async def delete_worker(
    worker_id: WorkerID, session: SessionDep, check: AdminRequieredDep
):
    await WorkersProcessor.delete_worker_from_db(worker_id, session)
    return {"success": True}


@router.patch("/{worker_id}", summary="Внести изменения в атрибуты работника из БД")
async def update_worker(
    worker_id: WorkerID, new_data: WorkerPatchSchema, session: SessionDep
):
    changed_rows = await WorkersProcessor.patch_worker_from_db(
        worker_id, new_data.model_dump(), session
    )
    return {"success": True, "changed_rows": changed_rows}


@router.get(
    "/{worker_id}",
    response_model=WorkerGetSchemaWithResume | dict,
    summary="Получить конкретного работника из БД",
)
async def get_concrete_worker(worker_id: int, session: SessionDep):
    result = await WorkersProcessor.get_concrete_worker_from_db(worker_id, session)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="worker wasn not found"
        )
    return result
