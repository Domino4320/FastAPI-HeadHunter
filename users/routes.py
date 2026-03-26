from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
from .crud import get_current_user, oauth2_scheme, fake_db, hashfunc_imitation
from .schemas import UserSchema, UserInDB


router = APIRouter(prefix="/private", tags=["Приватные пути"])


@router.get("/current", summary="Получить текущего пользователя")
async def get_current_user(user: Annotated[UserSchema, Depends(get_current_user)]):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="user not founded"
        )
    return user


@router.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user_dict = fake_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password",
        )
    user = UserInDB(**user_dict)
    hashed_password = hashfunc_imitation(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password",
        )
    return {"access_token": user.username, "token_type": "bearer"}
