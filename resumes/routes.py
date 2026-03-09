from fastapi import APIRouter
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


@router.get("/", response_model=List[ResumeGetSchemaWithWorker])
async def get_resumes(session: SessionDep):
    results = await ResumeProcessor.get_resumes_from_db(session)
    return results


@router.post("/")
async def post_resume(session: SessionDep, data: ResumePostSchema):
    await ResumeProcessor.insert_resume_into_db(session, data)
    return {"success": True}


@router.delete("/{resume_id}")
async def delete_resume(session: SessionDep, resume_id: int):
    await ResumeProcessor.delete_resume_from_db(session, resume_id)
    return {"success": True}


@router.patch("/{resume_id}")
async def patch_resume(
    session: SessionDep, resume_id: int, new_data: ResumePatchSchema
):
    await ResumeProcessor.patch_resume_into_db(
        session, resume_id, new_data.model_dump()
    )
