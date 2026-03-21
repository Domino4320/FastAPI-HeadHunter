from sqlalchemy import (
    CheckConstraint,
    DateTime,
)
from core.models import BaseWithTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import and_
from enum import Enum
from datetime import datetime, timezone
from typing import Annotated
from core.enums import City, Status, Specialization
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from core.models.vacancy_response import VacancyResponse
    from core.models.resume import Resume


class Worker(BaseWithTime):
    username: Mapped[str] = mapped_column(nullable=False)
    age: Mapped[int] = mapped_column(nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
    city: Mapped[City] = mapped_column(nullable=False)
    status: Mapped[Status] = mapped_column(nullable=False, default=Status.NOT_LOOKING)
    specialization: Mapped[Specialization] = mapped_column(nullable=True)
    resume: Mapped[List["Resume"]] = relationship(back_populates="worker")
    vacancy_responses: Mapped[List["VacancyResponse"]] = relationship(
        back_populates="worker"
    )
    # back_populates синхронизирует объекты в памяти в двух таблицах
    __table_args__ = (CheckConstraint(and_(age >= 18, age <= 110), name="check_age"),)

    # sqlalchemy берет ключи из Enum и по ним в БД создает свой Enum
