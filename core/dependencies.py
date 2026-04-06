from core.database import db_context
from typing import Annotated
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from core.security import oauth2_scheme
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError
from users.crud import TokenManager
from core.enums import Role
from fastapi.security import OAuth2PasswordRequestForm

SessionDep = Annotated[AsyncSession, Depends(db_context.get_session)]
TokenDep = Annotated[str, Depends(oauth2_scheme)]
FormDataDep = Annotated[OAuth2PasswordRequestForm, Depends()]


async def get_payload(token: TokenDep):
    try:
        return TokenManager.get_payload_from_token(token)
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Expired token"
        )


async def is_admin(payload: Annotated[dict, Depends(get_payload)], session: SessionDep):
    if not payload.get("role") == Role.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Denied access"
        )
    return payload


AdminRequieredDep = Annotated[dict, Depends(is_admin)]
