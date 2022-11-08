from uuid import UUID
from datetime import datetime

from pydantic import BaseModel


class PermissionInput(BaseModel):
    role_uuid: UUID
    entity_uuid: UUID
    can_read: bool = True
    can_write: bool = False

    class Config:
        orm_mode = True


class PermissionResponse(BaseModel):
    role_uuid: UUID
    entity_uuid: UUID
    can_read: bool = True
    can_write: bool = False

    created_at: datetime
    updated_at: datetime | None

    class Config:
        orm_mode = True
