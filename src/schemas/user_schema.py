import datetime

from pydantic import BaseModel


class UserBase(BaseModel):
    uuid: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    deleted_at: datetime.datetime

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    name: str
    surname: str

    class Config:
        orm_mode = True


class UserResponse(UserBase, UserCreate):
    pass
