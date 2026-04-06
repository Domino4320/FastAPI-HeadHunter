from .settings import crypt_settings
from .schemas import UserRegistrationSchema, TokenData, Token, UserLoginSchema
from core.utils import Hasher
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from core.models.users import User
from core.enums import Role
import jwt
from datetime import timedelta, datetime, timezone


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

    async def register_user(self, role: Role = None):

        await self._check_user_data_availability()
        self.user.password = Hasher.hash_password(self.user.password)
        if role:
            data = self.user.model_dump()
            data.update({"role": role})
            self.session.add(User(**data))
        else:
            self.session.add(User(**self.user.model_dump()))
        await self.session.commit()


class TokenManager:

    @staticmethod
    def generate_token(data: TokenData):
        token = jwt.encode(
            payload=data.model_dump(),
            key=crypt_settings.SECRET_KEY,
            algorithm=crypt_settings.ALGORITHM,
        )
        return Token(access_token=token, token_type="bearer")

    @staticmethod
    def get_payload_from_token(token: str):
        payload = jwt.decode(
            jwt=token,
            key=crypt_settings.SECRET_KEY,
            algorithms=[crypt_settings.ALGORITHM],
        )
        return payload


class AuthError(Exception):
    def __init__(self, message: str = None):
        self.message = message
        super().__init__(message)


class Authenticator:

    def __init__(self, data: UserLoginSchema, session: AsyncSession):
        self.data = data
        self.session = session

    async def _verify_user(self) -> User:
        query = select(User).where(User.login == self.data.login)
        raw_user = await self.session.execute(query)
        user = raw_user.scalar_one_or_none()
        if user and Hasher.verify_password(self.data.password, user.password):
            return user
        raise AuthError("Incorrect login or password")

    async def authenticate(self):
        user = await self._verify_user()
        payload = TokenData(
            login=user.login,
            exp=datetime.now(timezone.utc)
            + timedelta(minutes=crypt_settings.ACCESS_TOKEN_EXPIRE_MINUTES),
            role=user.role,
        )
        return TokenManager.generate_token(payload)
