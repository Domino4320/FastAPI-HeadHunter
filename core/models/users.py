from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import CheckConstraint
from .base import BaseWithTime
from core.enums import Role


class User(BaseWithTime):
    username: Mapped[str] = mapped_column(nullable=False)
    login: Mapped[str] = mapped_column(nullable=False, unique=True, index=True)
    password: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=True, unique=True)
    role: Mapped[Role] = mapped_column(
        nullable=False, default=Role.USER, server_default="USER"
    )

    __table_args__ = (
        CheckConstraint("LENGTH(username) >= 8 AND LENGTH(username) <= 50"),
        CheckConstraint("LENGTH(login) >= 8 AND LENGTH(login) <= 50"),
        CheckConstraint("LENGTH(email) <= 200"),
    )
