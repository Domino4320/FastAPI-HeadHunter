from fastapi import APIRouter, HTTPException
from resumes.crud import ResumeProcessor
from core.dependencies import SessionDep
from resumes.schemas import (
    ResumePostSchema,
    ResumeGetSchemaWithWorker,
    ResumePatchSchema,
)
from workers.schemas import WorkerGetSchema
from typing import List

ResumeGetSchemaWithWorker.model_rebuild()

router = APIRouter(prefix="/resumes", tags=["Резюме"])


@router.get(
    "/",
    response_model=List[ResumeGetSchemaWithWorker],
    summary="Получить все резюме работников из БД",
)
async def get_resumes(session: SessionDep):
    results = await ResumeProcessor.get_resumes_from_db(session)
    return results


@router.post("/", summary="Отправить резюме работника в БД")
async def post_resume(session: SessionDep, data: ResumePostSchema):
    await ResumeProcessor.insert_resume_into_db(session, data)
    return {"success": True}


@router.delete("/{resume_id}", summary="Удалить резюме работника из БД")
async def delete_resume(session: SessionDep, resume_id: int):
    await ResumeProcessor.delete_resume_from_db(session, resume_id)
    return {"success": True}


@router.patch("/{resume_id}", summary="Внести изменения в резюме работника из БД")
async def patch_resume(
    session: SessionDep, resume_id: int, new_data: ResumePatchSchema
):
    await ResumeProcessor.patch_resume_into_db(
        session, resume_id, new_data.model_dump()
    )


@router.get(
    "/{resume_id}",
    summary="Получить конкретное резюме работника из БД",
    response_model=ResumeGetSchemaWithWorker,
)
async def get_concrete_resume(session: SessionDep, resume_id: int):
    resume = await ResumeProcessor.get_concrete_resume_from_db(session, resume_id)
    if resume is None:
        raise HTTPException(status_code=404, detail="resume was not found")
    return resume
