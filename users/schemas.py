from pydantic import BaseModel


class UserSchema(BaseModel):
    username: str
    email: str | None = None
    phone: str | None = None


class UserInDB(UserSchema):
    hashed_password: str


class Token(BaseModel):
    access_token: str
    token_type: str
