from typing import Annotated
from fastapi import APIRouter, HTTPException, Depends, Path
from schemas import UserResponse, UserCreate
from models import User
from sqlalchemy.ext.asyncio import AsyncSession
from db import db_helper
from services import users as user_service
from errors import UserNotFound, UserAlreadyExists
from dto import ResponseMessage

user_router = APIRouter(prefix="/users", tags=["Users"])


@user_router.get("/", response_model=list[UserResponse])
async def get_users(db: AsyncSession = Depends(db_helper.get_db)) -> list[UserResponse]:
    users = await user_service.get_users(db)

    return [UserResponse.model_validate(user) for user in users]


@user_router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: Annotated[
        int,
        Path(..., ge=1, lt=1_000_000),
    ],
    db: AsyncSession = Depends(db_helper.get_db),
) -> UserResponse:
    try:
        user: User = await user_service.get_user(user_id, db)
    except UserNotFound as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )

    return UserResponse.model_validate(user)


@user_router.post("/", response_model=UserResponse)
async def create_user(
    new_user: UserCreate,
    db: AsyncSession = Depends(db_helper.get_db),
) -> UserResponse:
    try:
        user: User = await user_service.create_user(new_user, db)
    except UserAlreadyExists as exc:
        raise HTTPException(
            status_code=201,
            detail=str(exc),
        )

    return UserResponse.model_validate(user)


@user_router.delete("/{user_id}", response_model=ResponseMessage)
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(db_helper.get_db),
) -> ResponseMessage:
    try:
        result: ResponseMessage = await user_service.delete_user(user_id, db)
    except UserNotFound as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )

    return ResponseMessage.model_validate(result)
