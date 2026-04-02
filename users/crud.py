from fastapi import Depends, HTTPException, status
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer
from .settings import crypt_settings
from pwdlib import PasswordHash
from datetime import timedelta, datetime
import jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="private/token")

fake_db = {
    "John": {
        "username": "John",
        "email": "john@gmail.com",
        "phone": "+375298169348",
        "hashed_password": "hash_12345678",
    },
    "Bob": {
        "username": "Bob",
        "email": "Bob@gmail.com",
        "phone": None,
        "hashed_password": "hash_1234567890",
    },
}


class PasswordProcessor:

    password_hasher = PasswordHash.recommended()
    DUMMY_HASH = password_hasher.hash("dummy_passsword")

    @classmethod
    def hash_password(cls, password: str) -> str:
        return cls.password_hasher.hash(password)

    @classmethod
    def verify_password(cls, plain_password, hashed_password):
        return cls.hash_password(plain_password) == hashed_password

    @classmethod
    def dummy_verifying(cls, password):
        cls.hash_password(password) == cls.DUMMY_HASH


class Authenticator:

    @staticmethod
    def authenticate_user(username: str, password: str):
        user = fake_db.get(username)
        if not user:
            PasswordProcessor.dummy_verifying(password)
            return False
        if PasswordProcessor.verify_password(password):
            return user
        return False

    @staticmethod
    def create_access_token(data: dict):
        to_encode = data.copy()
        expire = datetime.now() + timedelta(
            minutes=crypt_settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            payload=to_encode,
            key=crypt_settings.SECRET_KEY,
            algorithm=crypt_settings.ALGORITHM,
        )
        return encoded_jwt


# def get_current_user(token : Annotated[str ,Depends[oauth2_scheme]]) -> UserSchema:
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate" : "Bearer"}
#     )
#     try:
#         payload = jwt.decode(jwt=token, key=crypt_settings.SECRET_KEY, algorithms = [crypt_settings.ALGORITHM],)
#     except InvalidTokenError
