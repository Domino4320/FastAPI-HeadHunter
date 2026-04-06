from pydantic import BaseModel, EmailStr, Field, field_validator, PrivateAttr
from core.utils import LoginValidationStrategy, PasswordValidationStrategy
from core.enums import Role
from typing import Annotated
from datetime import datetime

DefaultInputField = Annotated[str, Field(min_length=8, max_length=50)]


class UserRegistrationSchema(BaseModel):
    username: DefaultInputField
    login: DefaultInputField
    password: DefaultInputField
    email: EmailStr | None = Field(None, max_length=200)

    @field_validator("login")
    @classmethod
    def validate_login(cls, v: str) -> str:
        LoginValidationStrategy.validate(v)
        return v

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        PasswordValidationStrategy.validate(v)
        return v


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    login: str
    role: Role
    exp: datetime


class UserLoginSchema(BaseModel):
    login: str
    password: str
