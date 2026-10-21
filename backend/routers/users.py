from fastapi import APIRouter, Depends, HTTPException
from schemas import UserResponse, UserCreate
from sqlalchemy.ext.asyncio import AsyncSession
from db import db_helper
from services import users as crud_users

users_router = APIRouter(prefix="/users", tags=["Users"])


@users_router.get("/", response_model=list[UserResponse])
async def get_users(db: AsyncSession = Depends(db_helper.get_db)) -> list[UserResponse]:
    users = await crud_users.get_users(db)

    return [UserResponse.model_validate(user) for user in users]
