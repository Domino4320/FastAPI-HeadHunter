from pydantic import BaseModel, Field, model_validator
from typing import Self


class WorkerBase(BaseModel):
    username: str = Field(min_length=8, max_length=50)
    age: int = Field(ge=18, le=110)


class WorkerPostSchema(WorkerBase):
    pass


class WorkerPatchSchema(WorkerBase):

    @model_validator(mode="after")
    def check_changes_availability(self) -> Self:
        if not self.model_dump(exclude_unset=True):
            raise ValueError("Хотя бы одно значение должно меняться обязательно")
        return self


class WorkerGetSchema(WorkerBase):
    id: int
