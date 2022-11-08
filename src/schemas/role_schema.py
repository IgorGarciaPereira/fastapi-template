from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class RoleBase(BaseModel):
    uuid: UUID

    class Config:
        orm_mode = True


class RoleInput(BaseModel):
    name: str
    deletable: bool = True

    class Config:
        orm_mode = True


class RoleResponse(RoleBase):
    name: str
    deletable: bool
    created_at: datetime
    updated_at: datetime | None
