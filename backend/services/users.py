from collections.abc import Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from models import User
from repositories import users as crud_users
from errors import UserNotFound, UserAlreadyExists
from schemas import UserCreate, UserResponse, UserUpdate
from dto import ResponseMessage


async def get_users(db: AsyncSession) -> Sequence[User]:
    users: Sequence[User] = await crud_users.get_users(db)

    return users


async def get_user(user_id: int, db: AsyncSession) -> User:
    user: User | None = await crud_users.get_user(user_id, db)

    if user is None:
        raise UserNotFound(user_id=user_id)

    return user


async def create_user(new_user: UserCreate, db: AsyncSession) -> User:
    user = await crud_users.get_user_by_email(email=new_user.email, db=db)

    if user is not None:
        raise UserAlreadyExists(email=new_user.email)

    user = User(
        first_name=new_user.first_name,
        last_name=new_user.last_name,
        email=new_user.email,
        password_hash=new_user.password_hash,
    )

    user = await crud_users.create_user(user, db)

    return user


async def delete_user(user_id: int, db: AsyncSession) -> ResponseMessage:
    user: User | None = await crud_users.get_user(user_id, db)

    if user is None:
        raise UserNotFound(user_id=user_id)

    response = await crud_users.delete_user(user, db)

    return response


async def update_user(user_id: int, new_user: UserUpdate, db: AsyncSession) -> User:
    user: User | None = await crud_users.get_user(user_id, db)

    if user is None:
        raise UserNotFound(user_id=user_id)

    check_email = await crud_users.get_user_by_email(email=new_user.email, db=db)

    if check_email is not None:
        raise UserAlreadyExists(email=new_user.email)

    user.email = new_user.email
    user.first_name = new_user.first_name
    user.last_name = new_user.last_name

    user = await crud_users.update_user(user, db)

    return user
