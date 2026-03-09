from pydantic import BaseModel, Field, model_validator
from typing import Self
from core.utils import City, Specialization, Status
from typing import List
from core.utils import check_changes_availability as utils_check


class WorkerBase(BaseModel):
    username: str = Field(min_length=8, max_length=50)
    age: int = Field(ge=18, le=110)
    city: City
    specialization: Specialization
    status: Status | None = Field(None)


class WorkerPostSchema(WorkerBase):
    pass


class WorkerPatchSchema(WorkerBase):

    @model_validator(mode="after")
    def check_changes_availability(self) -> Self:
        utils_check()


class WorkerGetSchema(WorkerBase):
    id: int


class WorkerGetSchemaWithResume(WorkerGetSchema):
    resume: List["ResumeGetSchema"]
