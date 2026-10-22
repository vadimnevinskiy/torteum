from typing import Annotated
from fastapi import Depends, HTTPException, status
from models import User
from sqlalchemy.ext.asyncio import AsyncSession
from db.db_helper import db_helper
from services import users as crud_users
from errors import UserNotFound


async def get_user_by_id(
    user_id: int, db: AsyncSession = Depends(db_helper.get_db)
) -> User:
    try:
        user = await crud_users.get_user(user_id, db)
    except UserNotFound as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

    return user
