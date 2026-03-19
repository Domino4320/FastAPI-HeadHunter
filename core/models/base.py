from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column
from sqlalchemy import String, DateTime, func
from datetime import datetime, timezone


class Base(DeclarativeBase):
    __abstract__ = True

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    id: Mapped[int] = mapped_column(primary_key=True)


class BaseWithTime(Base):
    __abstract__ = True

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        server_default=func.now(),
        nullable=False,
    )
