from pydantic import BaseModel, field_validator, EmailStr
from datetime import datetime


class UserBase(BaseModel):
    first_name: str
    last_name: str | None = None
    avatar_url: str | None = None
    email: EmailStr

    @field_validator("last_name", mode="before")
    @classmethod
    def empty_last_name_to_none(cls, value):
        if isinstance(value, str) and not value.strip():
            return None
        return value


class UserCreate(UserBase):
    password_hash: str


class UserUpdate(UserBase):
    pass


class UserUpdatePartial(UserBase):
    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr | None = None
    avatar_url: str | None = None


class UserResponse(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
