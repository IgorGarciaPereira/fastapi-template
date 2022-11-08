from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class UserBase(BaseModel):
    uuid: UUID
    created_at: datetime
    updated_at: datetime | None

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    name: str
    surname: str
    role_uuid: str | None

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    name: str | None
    surname: str | None
    role_uuid: str | None

    class Config:
        orm_mode = True


class UserCreated(BaseModel):
    uuid: UUID

    class Config:
        orm_mode = True


class UserResponse(UserBase, UserCreate):
    name: str | None
    surname: str | None
    role_uuid: UUID | None
