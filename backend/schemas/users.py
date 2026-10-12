from typing import Annotated
from annotated_types import MinLen, MaxLen
from pydantic import BaseModel, EmailStr
from datetime import datetime


class UserBase(BaseModel):
    first_name: Annotated[str, MinLen(5), MaxLen(150)]
    last_name: Annotated[str, MaxLen(150)]
    email: EmailStr
    password_hash: Annotated[str, MinLen(6), MaxLen(250)]


class UserCreate(UserBase):
    pass


class UserResponse(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
