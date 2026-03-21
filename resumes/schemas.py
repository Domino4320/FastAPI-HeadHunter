from pydantic import Field, HttpUrl, AfterValidator, model_validator
from core.enums import Education
from typing import Annotated, Self
from pydantic import BaseModel, PlainSerializer
from core.utils import check_changes_availability as utils_check
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from workers.schemas import WorkerGetSchema


def validate_porfolio_url(url: HttpUrl) -> HttpUrl:
    if url.host in ["hh.ru", "linkedin.com", "www.linkedin.com"]:
        return url
    raise ValueError("Link must contains 'hh.ru' or 'linkedin")


def serialize_url(url: HttpUrl) -> str:
    return str(url)


class ResumeBase(BaseModel):
    about_me: str = Field(max_length=1000)
    experience_years: int = Field(ge=0)
    salary_expectations: int = Field(ge=1000)
    portfolio_url: Annotated[HttpUrl, AfterValidator(validate_porfolio_url)] | None = (
        Field(None)
    )
    education: Education
    education_status: bool
    educational_institute: str = Field(max_length=200)
    extra_info: str = Field(max_length=500)


class ResumeSchemaWithWorkerId(ResumeBase):
    worker_id: int = Field(ge=1)


class ResumeGetSchema(ResumeSchemaWithWorkerId):
    id: int


class ResumeGetSchemaWithWorker(ResumeSchemaWithWorkerId):
    worker: "WorkerGetSchema"


class ResumePostSchema(ResumeSchemaWithWorkerId):
    portfolio_url: (
        Annotated[
            HttpUrl,
            AfterValidator(validate_porfolio_url),
            PlainSerializer(serialize_url),
        ]
        | None
    ) = Field(None)


class ResumePatchSchema(ResumeBase):

    @model_validator(mode="after")
    def check_changes_availability(self) -> Self:
        utils_check(self)
        return self
