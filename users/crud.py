from fastapi import Depends
from typing import Annotated
from .schemas import UserSchema
from fastapi.security import OAuth2PasswordBearer

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


def decode_token(token: Annotated[str, Depends(oauth2_scheme)]) -> UserSchema:
    return UserSchema(
        username="John",
        email="john@gmail.com",
        phone="+375298978675",
    )


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = decode_token(token)
    return user


def hashfunc_imitation(password: str) -> str:
    return "hash_" + password


def get_user(username: str) -> UserSchema | None:
    return UserSchema(user := fake_db.get(username)) if not user is None else None
