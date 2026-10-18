from pydantic import BaseModel
from datetime import datetime


class UserBase(BaseModel):
    first_name: str
    last_name: str | None = None
    email: str
    password_hash: str


class UserCreate(UserBase):
    pass


class UserResponse(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime
