from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class UserBase(BaseModel):
    uuid: UUID
    created_at: datetime
    updated_at: datetime | None
    deleted_at: datetime | None

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    name: str
    surname: str

    class Config:
        orm_mode = True


class UserResponse(UserBase, UserCreate):
    pass
