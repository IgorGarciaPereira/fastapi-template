from fastapi import Request, HTTPException

from src.controllers.auth_controller import validate_token


async def is_authenticated(request: Request):
    authorization = request.headers.get('authorization')

    if not authorization:
        raise HTTPException(status_code=401, detail='Not authenticated')

    authorization = authorization.split('Bearer ')[1]
    validate_token(authorization)
    return True
