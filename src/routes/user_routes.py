from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.controllers.user_controller import UserController
from src.database.settings import get_db
from src.schemas.user_schema import UserCreate, UserResponse

user_router = APIRouter(prefix='/user', tags=['User'])


@user_router.get('', response_model=List[UserResponse])
def get_list_users(skip: int = 0, limit: int = 25, db: Session = Depends(get_db)):
    return UserController().handle_list(db, skip, limit)


@user_router.get('/{user_uuid}', response_model=UserResponse)
def get_a_user(user_uuid: str, db: Session = Depends(get_db)):
    return UserController().handle_get(db, user_uuid)


@user_router.post('', status_code=201)
def post_user(user: UserCreate, db: Session = Depends(get_db)):
    return UserController().handle_create(db, user)


@user_router.delete('/{user_uuid}', status_code=204)
def delete_user(user_uuid: str, db: Session = Depends(get_db)):
    return UserController().handle_delete(db, user_uuid, True)


@user_router.patch('/{user_uuid}', status_code=204)
def patch_user(user_uuid: str, data: UserCreate, db: Session = Depends(get_db)):
    return UserController().handle_patch(db, user_uuid, data)
