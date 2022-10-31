import uuid, datetime

from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.controllers.user_controller import UserController
from src.database.models.user_model import User
from src.database.settings import get_db
from src.schemas.user_schema import UserCreate, UserResponse

user_router = APIRouter(prefix='/user')


@user_router.get('', response_model=List[UserResponse])
def get_list_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return UserController().handle_list(db, skip, limit)


@user_router.post('')
def post_user(user: UserCreate, db: Session = Depends(get_db)):
    agora = datetime.datetime.now()
    db_user = User(name=user.name, surname=user.surname, uuid=uuid.uuid4(), created_at=agora)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
