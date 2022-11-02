import os
from datetime import timedelta, datetime
from uuid import uuid4

from fastapi import HTTPException
from jose import jwt, ExpiredSignatureError
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from src.controllers.base_controller import BaseController
from src.controllers.user_controller import UserController
from src.crud.auth_crud import AuthCrud
from src.schemas.auth_schema import AuthCreate, AuthLogin


def create_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        os.getenv('SECRET_KEY'),
        algorithm=os.getenv('ALGORITHM')
    )
    return {'access_token': encoded_jwt, 'token_type': 'Bearer'}


def validate_token(token: str):
    key = os.getenv('SECRET_KEY')
    algorithm = os.getenv('ALGORITHM')
    try:
        jwt.decode(token, key, algorithm)
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail='Authentication expired')


class AuthController(BaseController):
    def __init__(self):
        super(AuthController, self).__init__(crud_class=AuthCrud)
        self.pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")

    def __verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def __get_password_hash(self, password):
        return self.pwd_context.hash(password)

    def handle_register(self, db: Session, data: AuthCreate, commit=True):
        hash_password = self.__get_password_hash(data.password)
        data.password = hash_password

        user_uuid = uuid4()
        user = UserController().handle_create(db, {'uuid': user_uuid}, False)

        data = dict(data).copy()
        data['user_uuid'] = user_uuid

        self.handle_create(db, data, False)

        if commit:
            db.commit()
        return user

    def handle_login(self, db: Session, data: AuthLogin):
        auth = self.handle_filter(db, default_return=False, email=data.email)
        if auth is None:
            raise HTTPException(status_code=401, detail='User or password invalid')
        elif not self.__verify_password(data.password, auth.password):
            raise HTTPException(status_code=401, detail='User or password invalid')

        token_data = {
            'uuid': f'{auth.user_uuid}',
            'name': auth.user.name
        }
        return create_token(token_data)
