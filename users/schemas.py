from pydantic import BaseModel, EmailStr, Field, field_validator


class UserBase(BaseModel):
    username: str = Field(max_length=50)


class UserBaseWithID(UserBase):
    id: int


class UserGetSchema(UserBaseWithID):
    email: str
    login: str


class UserPostSchema(UserBase):
    email: EmailStr | None = Field(None)
    login: str = Field(max_length=30, pattern=r"")
    password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        if not re.search(r"[A-Z]", value):
            ...


class Token(BaseModel):
    access_token: str
    token_type: str
