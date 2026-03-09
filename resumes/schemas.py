from pydantic import Field, HttpUrl, AfterValidator
from core.utils import Education
from typing import Annotated
from pydantic import BaseModel, PlainSerializer


def validate_porfolio_url(url: HttpUrl) -> HttpUrl:
    if url.host == "hh.ru" or url.host == "linkedin.com":
        return url
    raise ValueError("Link must contains 'hh.ru' or 'lindein")


def serialize_url(url: HttpUrl) -> str:
    return str(url)


class ResumeBase(BaseModel):
    worker_id: int = Field(ge=1)
    about_me: str = Field(max_length=1000)
    experience_years: int = Field(ge=0)
    salary_expectations: int = Field(ge=1000)
    portfolio_url: Annotated[HttpUrl, AfterValidator(validate_porfolio_url)]
    education: Education
    education_status: bool
    educational_institute: str = Field(max_length=200)
    extra_info: str = Field(max_length=500)


class ResumeGetSchema(ResumeBase):
    id: int


class ResumeGetSchemaWithWorker(ResumeGetSchema):
    worker: "WorkerGetSchema"


class ResumePostSchema(ResumeBase):
    portfolio_url: Annotated[
        HttpUrl, AfterValidator(validate_porfolio_url), PlainSerializer(serialize_url)
    ]
