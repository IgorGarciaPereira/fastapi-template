from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session

from src.controllers.auth_controller import validate_token, AuthController
from src.database.settings import get_db
from src.schemas.auth_schema import Token, AuthCreate, AuthLogin

auth_router = APIRouter(prefix='/auth', tags=['Auth'])


@auth_router.post('/login', response_model=Token)
def handle_login(data: AuthCreate, db: Session = Depends(get_db)):
    return AuthController.handle_login(db, data)


@auth_router.get('/check-token')
def handle_validate_token(req: Request):
    token: str = req.headers.get('authorization')
    token = token.split('Bearer ')[1]
    return validate_token(token)


@auth_router.post('/register', status_code=201)
def handle_register(data: AuthLogin, db: Session = Depends(get_db)):
    return AuthController().handle_register(db, data)
