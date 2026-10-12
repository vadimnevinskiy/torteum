from collections.abc import Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from models import User
from schemas import UserCreate
from repositories import users as crud
from errors import UserNotFound, UserAlreadyExists
from dto import ResponseMessage


async def get_users(db: AsyncSession) -> Sequence[User]:
    users: Sequence[User] = await crud.get_users(db)

    return users


async def get_user(user_id: int, db: AsyncSession) -> User:
    user: User | None = await crud.get_user(user_id, db)

    if user is None:
        raise UserNotFound(user_id=user_id)

    return user


async def create_user(new_user: UserCreate, db: AsyncSession) -> User:
    exists_user: User | None = await crud.get_user_by_email(new_user.email, db)

    if exists_user is not None:
        raise UserAlreadyExists(email=new_user.email)

    user = User(
        first_name=new_user.first_name,
        last_name=new_user.last_name,
        email=new_user.email,
        password_hash=new_user.password_hash,
    )

    user: User = await crud.create_user(user, db)

    return user


async def delete_user(user_id: int, db: AsyncSession) -> ResponseMessage:
    user: User | None = await crud.get_user(user_id, db)

    if user is None:
        raise UserNotFound(user_id=user_id)

    result = await crud.delete_user(user, db)

    return result
