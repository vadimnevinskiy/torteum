from collections.abc import Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from models import User
from repositories import users as crud_users
from errors import UserNotFound, UserAlreadyExists
from schemas import UserCreate, UserResponse


async def get_users(db: AsyncSession) -> Sequence[User]:
    users: Sequence[User] = await crud_users.get_users(db)

    return users


async def get_user(user_id: int, db: AsyncSession) -> User:
    user: User | None = await crud_users.get_user(user_id, db)

    if user is None:
        raise UserNotFound(user_id=user_id)

    return user


async def create_user(new_user: UserCreate, db: AsyncSession) -> User:
    user = User(
        first_name=new_user.first_name,
        last_name=new_user.last_name,
        email=new_user.email,
        password_hash=new_user.password_hash,
    )

    user = await crud_users.create_user(user, db)

    return user
