from pydantic import BaseModel, Field
from core.enums import WorkFormat, Employment, Experience
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.models.vacancy_response import VacancyResponse


class VacancyBase(BaseModel):
    title: str
    requirements: str
    work_format: WorkFormat
    employment: Employment
    experience: Experience
    employer_contacts: str


class VacancyGetSchema(VacancyBase):
    id: int


class VacancyPostSchema(VacancyBase):
    requirements: str = Field(max_length=1000)


class VacancyGetSchemaWithVR(VacancyGetSchema):
    vacancy_responses: list["VacancyResponse"]
