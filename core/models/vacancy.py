from core.models.base import BaseWithTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import DateTime, CheckConstraint, func, text
from datetime import datetime, timezone
from core.enums import WorkFormat, Employment, Experience
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from core.models.vacancy_response import VacancyResponse


class Vacancy(BaseWithTime):
    title: Mapped[str] = mapped_column(nullable=False)
    requirements: Mapped[str] = mapped_column(nullable=False)
    work_format: Mapped[WorkFormat] = mapped_column(nullable=False)
    employment: Mapped[Employment] = mapped_column(nullable=False)
    experience: Mapped[Experience] = mapped_column(nullable=False)
    employer_contacts: Mapped[str] = mapped_column(nullable=False)
    vacancy_responses: Mapped[List["VacancyResponse"]] = relationship(
        back_populates="vacancy"
    )

    __table_args__ = (
        CheckConstraint(
            "length(requirements) <= 1000",
            name="check_requirements_length",
        ),
    )
