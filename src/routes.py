from src.schemas import WorkerPostSchema, ResumePostSchema, WorkerPatchSchema
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter
from src.queries.core import (DatabaseProcessor, WorkersProcessor, WorkersProcessor)

db_router = APIRouter(prefix="/database", tags=["БД"])

@db_router.get("/")
async def create_database():
    await DatabaseProcessor.create_tables()
    return {"success" : True}

workers_router = APIRouter(prefix="/workers", tags=["Работники"])

@workers_router.get("/", response_model=list[WorkerPostSchema], summary="Получить работника из БД")
async def get_workers():
    result = await WorkersProcessor.get_workers_from_db()
    return result

@workers_router.post("/", summary="Отправить работника в БД")
async def post_worker(data : WorkerPostSchema):
    await WorkersProcessor.insert_worker_into_db(data)
    return {"success" : True}

@workers_router.delete("/{id}", summary="Удалить работника из БД")
async def delete_worker():
    await WorkersProcessor.delete_worker_from_db(id)
    return {"success" : True}

@workers_router.patch("/{id}", summary="Внести изменения в атрибуты работника из БД")
async def update_worker(new_data : WorkerPatchSchema):
    changed_rows = await WorkersProcessor.patch_worker_from_db(id, new_data.model_dump(exclude_unset=True))
    return {"success" : True, "changed_rows" : changed_rows}




















# workers_router = APIRouter(prefix="/workers", tags=["Работники"])

# @workers_router.get("/")
# def get_workers():
#     return get_workers_from_db()

# @workers_router.post("/")
# def post_worker(data : WorkerPostSchema):
#     insert_worker_into_db(data)
#     return {"success" : True}

# resumes_router = APIRouter(prefix="/resumes", tags=["Резюме"])

# @resumes_router.get("/")
# def get_resumes():
#     return get_resumes_from_db()

# @resumes_router.post("/")
# def post_resume(data : ResumePostSchema):
#     insert_resume_into_db(data)
#     return {"success" : True}
    