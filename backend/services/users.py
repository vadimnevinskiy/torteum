from pathlib import Path
from fastapi import File, UploadFile
from collections.abc import Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from models import User
from repositories import users as crud_users
from errors import UserNotFound, UserAlreadyExists
from schemas import UserCreate, UserResponse, UserUpdate, UserUpdatePartial
from dto import ResponseMessage
from config import settings
from util import ImageHelper


async def get_users(db: AsyncSession) -> Sequence[User]:
    users: Sequence[User] = await crud_users.get_users(db)

    return users


async def get_user(user_id: int, db: AsyncSession) -> User:
    user: User | None = await crud_users.get_user(user_id, db)

    if user is None:
        raise UserNotFound(user_id=user_id)

    return user


async def create_user(new_user: UserCreate, db: AsyncSession) -> User:
    check_email = await crud_users.get_user_by_email(email=new_user.email, db=db)

    if check_email is not None:
        raise UserAlreadyExists(email=new_user.email)

    user = User(
        first_name=new_user.first_name,
        last_name=new_user.last_name,
        avatar_url=new_user.avatar_url,
        email=new_user.email,
        password_hash=new_user.password_hash,
    )

    user = await crud_users.create_user(user, db)

    return user


async def delete_user(user: User, db: AsyncSession) -> ResponseMessage:
    response = await crud_users.delete_user(user, db)

    return response


async def update_user(
    user: User,
    new_user: UserUpdate | UserUpdatePartial,
    db: AsyncSession,
    is_partial_update: bool = False,
) -> User:
    check_email = await crud_users.get_user_by_email(email=new_user.email, db=db)

    if check_email is not None and check_email.id != user.id:
        raise UserAlreadyExists(email=new_user.email)

    for name, value in new_user.model_dump(exclude_unset=is_partial_update).items():
        setattr(user, name, value)

    user = await crud_users.update_user(user, db)

    return user


async def upload_avatar(avatar: UploadFile) -> Path:
    helper = ImageHelper(
        image=avatar,
        image_path=settings.avatars_dir,
    )
    saved_path = await helper.save_image()
    return saved_path
