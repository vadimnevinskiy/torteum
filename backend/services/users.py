from collections.abc import Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from models import User
from repositories import users as crud
from errors import UserNotFound, UserAlreadyExists


async def get_users(db: AsyncSession) -> Sequence[User]:
    users: Sequence[User] = await crud.get_users(db)

    return users


async def get_user(user_id: int, db: AsyncSession) -> User:
    user: User | None = await crud.get_user(user_id, db)

    if user is None:
        raise UserNotFound(user_id=user_id)

    return user
