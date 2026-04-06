from fastapi import APIRouter, HTTPException, status
from .schemas import UserRegistrationSchema, UserLoginSchema, Token
from core.dependencies import SessionDep, FormDataDep
from .crud import Register, BusyDataError, AuthError, Authenticator


router = APIRouter(prefix="/security", tags=["Сервис распознавания пользователей"])


@router.post("/register")
async def register(data: UserRegistrationSchema, session: SessionDep):
    try:
        await Register(data, session).register_user()
    except BusyDataError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error.message,
        )
    return {"success": True}


@router.post("/auth", response_model=Token)
async def login(login_data: FormDataDep, session: SessionDep):
    user_data = UserLoginSchema(login=login_data.username, password=login_data.password)
    try:
        return await Authenticator(user_data, session).authenticate()
    except AuthError as ex:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=ex.message)
