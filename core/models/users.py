from sqlalchemy.orm import mapped_column, Mapped
from base import BaseWithTime


class User(BaseWithTime):
    username: Mapped[str] = mapped_column(nullable=False)
    login: Mapped[str] = mapped_column(nullable=False, unique=True)
    password: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=True, unique=True)
