from typing import Annotated
from fastapi import Depends, HTTPException, status, Path
from models import User
from sqlalchemy.ext.asyncio import AsyncSession
from db.db_helper import db_helper
from services import users as user_service
from errors import UserNotFound


async def get_user_by_id(
    user_id: Annotated[int, Path],
    db: Annotated[AsyncSession, Depends(db_helper.get_db)],
) -> User:
    try:
        user = await user_service.get_user(user_id, db)
    except UserNotFound as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )

    return user
