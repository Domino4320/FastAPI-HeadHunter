from core.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.enums import Education
from sqlalchemy import ForeignKey
from sqlalchemy import String, CheckConstraint
from pydantic import HttpUrl


class Resume(Base):
    worker_id: Mapped[int] = mapped_column(
        ForeignKey("worker.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False
    )
    worker: Mapped["Worker"] = relationship(back_populates="resume")
    about_me: Mapped[str] = mapped_column(String(1000), nullable=True)
    experience_years: Mapped[int] = mapped_column(
        nullable=False,
        default=0,
    )
    salary_expectations: Mapped[int] = mapped_column(nullable=True)
    portfolio_url: Mapped[str] = mapped_column(nullable=True)
    education: Mapped[Education] = mapped_column(nullable=False)
    education_status: Mapped[bool] = mapped_column(nullable=False)
    educational_institute: Mapped[str] = mapped_column(String(200), nullable=False)
    extra_info: Mapped[str] = mapped_column(String(500), nullable=True)

    __table_args__ = (
        CheckConstraint(experience_years >= 0, name="check_exp"),
        CheckConstraint(salary_expectations >= 1000, name="check_salary"),
    )
