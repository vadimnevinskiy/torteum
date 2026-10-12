from pydantic import BaseModel, EmailStr
from datetime import datetime


class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password_hash: str


class UserCreate(UserBase):
    pass


class UserResponse(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
