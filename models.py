from sqlalchemy import Table, Column, Integer, String, MetaData, Date, CheckConstraint, ForeignKey, text, cast, DateTime
from database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import and_
from enum import Enum
from datetime import datetime, timezone
from typing import Annotated

class WorkersOrm(Base):
    __tablename__ = "workers"
    id : Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username : Mapped[str] = mapped_column(nullable=False)
    registration_date : Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda : datetime.now(timezone.utc))
    age : Mapped[int] = mapped_column(nullable=False)
    updated_at : Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda : datetime.now(timezone.utc),
        onupdate=lambda : datetime.now(timezone.utc)),
    __table_args__ = (
        CheckConstraint(and_(age >= 18, age <= 110), name="check_age"),
    )

class Workload(Enum):
    parttime = "parttime"
    fulltime = "fulltime"

class ResumesOrm(Base):
    __tablename__ = "resumes"
    id : Mapped[int] = mapped_column(primary_key=True)
    title : Mapped[str] = mapped_column(String(256))
    salary : Mapped[int | None]
    workload : Mapped[Workload]
    worker_id : Mapped[int] = mapped_column(ForeignKey("workers.id", ondelete="CASCADE")) # Можно сделать SET NULL
    created_at : Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())")) # default задает на уровне Python c методами datetime
    updated_at : Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"), onupdate=datetime.now(timezone.utc))
    # с помощью Annotated можно создать кастомные типы и передавать их в Mapped[...]






























metadata_obj = MetaData()

workers_table = Table(
    "workers",
    metadata_obj,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("username", String, nullable=False),
    CheckConstraint("length(username) >= 8 and length(username) <= 50")
)