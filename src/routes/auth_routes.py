from fastapi import APIRouter, Request

from src.controllers.auth_controller import validate_token, create_token
from src.schemas.auth_schema import Token

auth_router = APIRouter(prefix='/auth', tags=['Auth'])


@auth_router.post('/login', response_model=Token)
def handle_login():
    # TODO: Get user from database
    data = dict({
        'user': 'Igor',
        'uuid': '7892345hasdf7'
    })
    return create_token(data)


@auth_router.get('/check-token')
def handle_validate_token(req: Request):
    token: str = req.headers.get('authorization')
    token = token.split('Bearer ')[1]
    return validate_token(token)
