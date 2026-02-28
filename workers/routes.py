from .schemas import WorkerPostSchema, WorkerPatchSchema
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter
from .crud import WorkersProcessor

router = APIRouter(prefix="/workers", tags=["Работники"])

@router.get("/", response_model=list[WorkerPostSchema], summary="Получить работника из БД")
async def get_workers():
    result = await WorkersProcessor.get_workers_from_db()
    return result

@router.post("/", summary="Отправить работника в БД")
async def post_worker(data : WorkerPostSchema):
    await WorkersProcessor.insert_worker_into_db(data)
    return {"success" : True}

@router.delete("/{id}", summary="Удалить работника из БД")
async def delete_worker():
    await WorkersProcessor.delete_worker_from_db(id)
    return {"success" : True}

@router.patch("/{id}", summary="Внести изменения в атрибуты работника из БД")
async def update_worker(new_data : WorkerPatchSchema):
    changed_rows = await WorkersProcessor.patch_worker_from_db(id, new_data.model_dump(exclude_unset=True))
    return {"success" : True, "changed_rows" : changed_rows}
    