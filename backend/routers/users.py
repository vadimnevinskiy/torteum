from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from schemas import UserResponse, UserCreate, UserUpdate, UserUpdatePartial
from models import User
from sqlalchemy.ext.asyncio import AsyncSession
from db import db_helper
from services import users as user_service
from errors import UserNotFound, UserAlreadyExists
from dto import ResponseMessage
from dependencies import get_user_by_id

users_router = APIRouter(prefix="/users", tags=["Users"])


@users_router.get("/", response_model=list[UserResponse])
async def get_users(db: AsyncSession = Depends(db_helper.get_db)) -> list[UserResponse]:
    users = await user_service.get_users(db)

    return [UserResponse.model_validate(user) for user in users]


@users_router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user: User = Depends(get_user_by_id),
) -> UserResponse:

    return UserResponse.model_validate(user)


@users_router.post("/", response_model=UserResponse)
async def create_user(
    new_user: UserCreate,
    db: AsyncSession = Depends(db_helper.get_db),
) -> UserResponse:
    try:
        user = await user_service.create_user(new_user, db)
    except UserAlreadyExists as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))

    return UserResponse.model_validate(user)


@users_router.delete("/{user_id}", response_model=ResponseMessage)
async def delete_user(
    user: Annotated[User, Depends(get_user_by_id)],
    db: Annotated[AsyncSession, Depends(db_helper.get_db)],
) -> ResponseMessage:
    try:
        response = await user_service.delete_user(user, db)
    except UserNotFound as exc:
        raise HTTPException(status_code=404, detail=str(exc))

    return ResponseMessage.model_validate(response)


@users_router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user: Annotated[User, Depends(get_user_by_id)],
    new_user: UserUpdate,
    db: Annotated[AsyncSession, Depends(db_helper.get_db)],
) -> UserResponse:
    try:
        user = await user_service.update_user(
            user, new_user, db, is_partial_update=False
        )
    except UserNotFound as exc_not_found:
        raise HTTPException(status_code=404, detail=str(exc_not_found))
    except UserAlreadyExists as exc_already_exists:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=str(exc_already_exists)
        )

    return UserResponse.model_validate(user)


@users_router.patch("/{user_id}", response_model=UserResponse)
async def update_user_partial(
    user: Annotated[User, Depends(get_user_by_id)],
    new_user: UserUpdatePartial,
    db: Annotated[AsyncSession, Depends(db_helper.get_db)],
) -> UserResponse:
    try:
        user = await user_service.update_user(
            user, new_user, db, is_partial_update=True
        )
    except UserNotFound as exc_not_found:
        raise HTTPException(status_code=404, detail=str(exc_not_found))
    except UserAlreadyExists as exc_already_exists:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=str(exc_already_exists)
        )

    return UserResponse.model_validate(user)
