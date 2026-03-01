from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, HTTPException, status, Path
from .crud import WorkersProcessor
from core.dependencies import SessionDep
from workers.schemas import WorkerGetSchema, WorkerPatchSchema, WorkerPostSchema
from typing import Annotated

router = APIRouter(prefix="/workers", tags=["Работники"])
WorkerID = Annotated[int, Path(gt=0)]
# Annotated перегружает магический метод __class_getitem__ в котором создает
# объект в который записывает тип как 1 атрибут объекта, а все остальные метаданные как другой


@router.get(
    "/", response_model=list[WorkerGetSchema], summary="Получить всех работников из БД"
)
async def get_workers(session: SessionDep):
    result = await WorkersProcessor.get_workers_from_db(session)
    return result


@router.post("/", summary="Отправить работника в БД")
async def post_worker(data: WorkerPostSchema, session: SessionDep):
    await WorkersProcessor.insert_worker_into_db(data, session)
    return {"success": True}


@router.delete("/{worker_id}", summary="Удалить работника из БД")
async def delete_worker(worker_id: WorkerID, session: SessionDep):
    await WorkersProcessor.delete_worker_from_db(id, session)
    return {"success": True}


@router.patch("/{worker_id}", summary="Внести изменения в атрибуты работника из БД")
async def update_worker(
    worker_id: WorkerID, new_data: WorkerPatchSchema, session: SessionDep
):
    changed_rows = await WorkersProcessor.patch_worker_from_db(
        id, new_data.model_dump(exclude_unset=True), session
    )
    return {"success": True, "changed_rows": changed_rows}


@router.get(
    "/{worker_id}",
    response_model=WorkerGetSchema | dict,
    summary="Получить конкретного работника из БД",
)
async def get_concrete_worker(worker_id: int, session: SessionDep):
    result = await WorkersProcessor.get_concrete_worker(worker_id, session)
    if result is not None:
        return result
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="worker wasn't found"
    )
