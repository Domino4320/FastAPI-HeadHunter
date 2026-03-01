from core.database import db_context
from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

SessionDep = Annotated[AsyncSession, Depends(db_context.get_session)]
