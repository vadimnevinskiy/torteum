from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from schemas import UserResponse, UserCreate, UserUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from db import db_helper
from services import users as crud_users
from errors import UserNotFound, UserAlreadyExists
from dto import ResponseMessage

users_router = APIRouter(prefix="/users", tags=["Users"])


@users_router.get("/", response_model=list[UserResponse])
async def get_users(db: AsyncSession = Depends(db_helper.get_db)) -> list[UserResponse]:
    users = await crud_users.get_users(db)

    return [UserResponse.model_validate(user) for user in users]


@users_router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(db_helper.get_db),
) -> UserResponse:
    try:
        user = await crud_users.get_user(user_id, db)
    except UserNotFound as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

    return UserResponse.model_validate(user)


@users_router.post("/", response_model=UserResponse)
async def create_user(
    new_user: UserCreate,
    db: AsyncSession = Depends(db_helper.get_db),
) -> UserResponse:
    try:
        user = await crud_users.create_user(new_user, db)
    except UserAlreadyExists as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))

    return UserResponse.model_validate(user)


@users_router.delete("/{user_id}", response_model=ResponseMessage)
async def delete_user(
    user_id: int,
    db: Annotated[AsyncSession, Depends(db_helper.get_db)],
) -> ResponseMessage:
    try:
        response = await crud_users.delete_user(user_id, db)
    except UserNotFound as exc:
        raise HTTPException(status_code=404, detail=str(exc))

    return ResponseMessage.model_validate(response)


@users_router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    new_user: UserUpdate,
    db: Annotated[AsyncSession, Depends(db_helper.get_db)],
) -> UserResponse:
    try:
        user = await crud_users.update_user(user_id, new_user, db)
    except UserNotFound as exc_not_found:
        raise HTTPException(status_code=404, detail=str(exc_not_found))
    except UserAlreadyExists as exc_already_exists:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=str(exc_already_exists)
        )

    return UserResponse.model_validate(user)
