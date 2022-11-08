import os

from fastapi import APIRouter, Depends, Request
from typing import List

from src.database.settings import get_db
from src.controllers.role_entity_controller import RoleEntityController
from src.middleware import is_authenticated, IsAuthorized
from src.schemas.permission_schema import PermissionInput, PermissionResponse

limit_default = int(os.getenv('LIMIT_LIST', 25))

is_authorized = IsAuthorized(entity='permissions')

permission_router = APIRouter(
    prefix='/permission',
    tags=['Permission'],
    dependencies=[Depends(is_authenticated), Depends(is_authorized)]
)


@permission_router.get('/', response_model=List[PermissionResponse])
def handle_list_permissions(request: Request, skip: int = 0, limit: int = limit_default, db=Depends(get_db)):
    filter_data = request.query_params
    return RoleEntityController().handle_list(db, skip, limit, **filter_data)


@permission_router.post('/', response_model=None, status_code=201)
def handle_create_permission(data: PermissionInput, db=Depends(get_db)):
    return RoleEntityController().handle_create(db, data)



