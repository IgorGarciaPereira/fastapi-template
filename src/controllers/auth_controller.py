import os
from datetime import timedelta, datetime
from uuid import uuid4, UUID

from fastapi import HTTPException
from jose import jwt, ExpiredSignatureError
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from typing import Any

from src.controllers.base_controller import BaseController
from src.controllers.user_controller import UserController
from src.crud.auth_crud import AuthCrud
from src.crud.role_crud import RoleCrud
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
        return jwt.decode(token, key, algorithm)
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
        auth = self.handle_filter(db, default_return=False, email=data.email, active=True)
        if auth is None:
            raise HTTPException(status_code=401, detail='User or password invalid')
        elif not self.__verify_password(data.password, auth.password):
            raise HTTPException(status_code=401, detail='User or password invalid')

        role = None
        role_uuid = auth.user.role_uuid or None
        if role_uuid:
            role = RoleCrud().get(db, uuid=role_uuid)

        token_data = {
            'uuid': f'{auth.user_uuid}',
            'name': auth.user.name,
            'role': role.name if role else None
        }
        return create_token(token_data)

    def handle_patch(self, db: Session, email: str, data: Any, commit=True):
        db_customer = self.crud_class().get(db, email=email)

        if db_customer is None:
            raise HTTPException(
                status_code=404,
                detail={'message': 'User not found'}
            )

        return self.crud_class().patch(db, email, data, commit)

    def handle_activate_user(self, db: Session, user_uuid: UUID):
        auth = AuthController().handle_list(db, 0, 1, user_uuid=user_uuid)
        if not len(auth):
            raise HTTPException(status_code=404, detail='User not found')
        auth = auth[0]
        return self.handle_patch(db, auth.email, {'active': True})
