from core.models.base import BaseWithTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.models.worker import Worker
    from core.models.vacancy import Vacancy


class VacancyResponse(BaseWithTime):
    worker_id: Mapped[int] = mapped_column(
        ForeignKey("worker.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False
    )
    vacancy_id: Mapped[int] = mapped_column(
        ForeignKey("vacancy.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False
    )
    worker: Mapped["Worker"] = relationship(back_populates="vacancy_response")
    vacancy: Mapped["Vacancy"] = relationship(back_populates="vacancy_response")
    message: Mapped[str] = mapped_column(nullable=True)
