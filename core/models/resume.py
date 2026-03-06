from core.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.utils import Education
from sqlalchemy import ForeignKey


class Resume(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    worker_id: Mapped[int] = mapped_column(ForeignKey("Worker.id"), nullable=False)
    worker: Mapped["Worker"] = relationship(back_populates="resume")
    about_me: Mapped[str] = mapped_column(nullable=True)
    experience_years: Mapped[int] = mapped_column(nullable=False, default=0)
    salary_expectations: Mapped[float] = mapped_column(nullable=True)
    portfolio_url: Mapped[str] = mapped_column(nullable=True)
    education: Mapped[Education] = mapped_column(nullable=False)
    education_status: Mapped[bool] = mapped_column(nullable=False)
    educational_institute: Mapped[str]
    extra_info: Mapped[str] = mapped_column(nullable=True)

    # Циклический импорт тут короче
