from fastapi import Depends, HTTPException, Request

from src.controllers.auth_controller import validate_token
from src.crud.role_entity_crud import RoleEntityCrud
from src.crud.role_crud import RoleCrud
from src.crud.entity_crud import EntityCrud
from src.database.settings import get_db


async def is_authenticated(request: Request):
    authorization = request.headers.get('authorization')

    if not authorization:
        raise HTTPException(status_code=401, detail='Not authenticated')

    authorization = authorization.split('Bearer ')[1]
    validate_token(authorization)
    return True


class IsAuthorized:
    def __init__(self, *, entity: str):
        self.entity = entity

    def __call__(self, request: Request, db=Depends(get_db)):
        authorization = request.headers.get('authorization')
        authorization = authorization.split('Bearer ')[1]
        token_data = validate_token(authorization)

        role_token = token_data.get('role')
        role: str = role_token.lower().capitalize() if role_token else None
        if role == 'Admin':
            return True

        role_db = RoleCrud().list(db, skip=0, limit=1, name=role)
        if not len(role_db):
            raise HTTPException(status_code=403, detail='Access forbidden')
        role_db = role_db[0]

        entity_db = EntityCrud().list(db, 0, 1, name=self.entity)
        if not len(entity_db):
            raise HTTPException(status_code=403, detail='Access forbidden')

        entity_db = entity_db[0]
        permission = RoleEntityCrud().list(db, 0, 1, role_uuid=role_db.uuid, entity_uuid=entity_db.uuid)

        if not len(permission):
            raise HTTPException(status_code=403, detail='Access forbidden')
        permission = permission[0]

        method = request.method
        write_methods = ['POST', 'PATCH', 'PUT', 'DELETE']
        read_methods = ['GET']

        if method in read_methods and permission.can_read:
            return True
        elif method in write_methods and permission.can_write:
            return True
        raise HTTPException(status_code=403, detail='Access forbidden')

