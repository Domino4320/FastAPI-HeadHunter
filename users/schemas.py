from pydantic import BaseModel, EmailStr, Field, field_validator
from core.utils import LoginValidationStrategy, PasswordValidationStrategy
from typing import Annotated

DefaultInputField = Annotated[str, Field(min_length=8, max_length=50)]


class UserRegistrationSchema(BaseModel):
    username: DefaultInputField
    login: DefaultInputField
    password: DefaultInputField
    email: EmailStr = Field(max_length=200)

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
