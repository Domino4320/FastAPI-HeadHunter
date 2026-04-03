from .settings import crypt_settings
from .schemas import UserRegistrationSchema
from core.utils import Hasher
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from core.models.users import User
import asyncio


class BusyDataError(Exception):
    def __init__(self, message: str = None):
        self.message = message
        super().__init__(self.message)


class Register:

    def __init__(self, data: UserRegistrationSchema, session: AsyncSession):
        self.user = data
        self.session = session

    async def _check_user_data_availability(self) -> None:
        login_query = select(User).where(User.login == self.user.login)
        login_check = await self.session.execute(login_query)
        email_query = select(User).where(User.email == self.user.email)
        email_check = await self.session.execute(email_query)
        if login_check.scalar():
            raise BusyDataError("login is busy")
        if email_check.scalar():
            raise BusyDataError("email is busy")

    async def register_user(self):
        await self._check_user_data_availability()
        self.user.password = Hasher.hash_password(self.user.password)
        self.session.add(User(**self.user.model_dump()))
        await self.session.commit()
