from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
from .crud import (
    oauth2_scheme,
    fake_db,
    Authenticator,
    PasswordProcessor,
)
from .schemas import UserRegistrationSchema
import jwt
from core.dependencies import SessionDep


router = APIRouter(prefix="/security", tags=["Приватные пути"])


# @router.get("/current", summary="Получить текущего пользователя")
# async def get_current_user(user: Annotated[UserSchema, Depends(get_current_user)]): ...


# @router.post("/token")
# async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
#     user_dict = Authenticator.authenticate_user(
#         username=form_data.username, password=form_data.password
#     )
#     if not user_dict:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Incorrect username or password",
#         )
#     user = UserPostSchema(**user_dict)
#     return {"access_token": user.username, "token_type": "bearer"}


@router.post("/register")
async def register(data: UserRegistrationSchema):
    return data
