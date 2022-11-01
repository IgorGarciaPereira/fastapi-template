from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    uuid: str
    name: str


class AuthCreate(BaseModel):
    email: EmailStr
    password: str

    class Config:
        orm_mode = True


class AuthLogin(AuthCreate):
    pass
