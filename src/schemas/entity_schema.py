from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class EntityBase(BaseModel):
    uuid: UUID
    created_at: datetime
    updated_at: datetime | None

    class Config:
        orm_mode = True


class Entity(EntityBase):
    name: str


class EntityInput(BaseModel):
    name: str

    class Config:
        orm_mode = True


class EntityCreated(BaseModel):
    uuid: UUID

    class Config:
        orm_mode = True
