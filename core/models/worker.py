from sqlalchemy import (
    Table,
    Column,
    Integer,
    String,
    MetaData,
    Date,
    CheckConstraint,
    ForeignKey,
    text,
    cast,
    DateTime,
)
from core.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import and_
from enum import Enum
from datetime import datetime, timezone
from typing import Annotated
from core.utils import City, Status, Specialization
from typing import List


class Worker(Base):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(nullable=False)
    registration_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
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
    # back_populates синхронизирует объекты в памяти в двух таблицах
    __table_args__ = (CheckConstraint(and_(age >= 18, age <= 110), name="check_age"),)

    # sqlalchemy берет ключи из Enum и по ним в БД создает свой Enum
