import os
from uuid import UUID

from fastapi import APIRouter, Depends, Request
from typing import List

from src.controllers.role_controller import RoleController
from src.database.settings import get_db
from src.middleware import is_authenticated, IsAuthorized
from src.schemas.role_schema import RoleBase, RoleResponse, RoleInput
limit_default = int(os.getenv('LIMIT_LIST', 25))


is_authorized = IsAuthorized(entity='roles')

role_router = APIRouter(
    prefix='/role',
    tags=['Role'],
    dependencies=[Depends(is_authenticated), Depends(is_authorized)]
)


@role_router.get('/', response_model=List[RoleResponse])
def handle_list_roles(req: Request, db=Depends(get_db), skip=0, limit=limit_default):
    filter_data = req.query_params
    return RoleController().handle_list(db, skip, limit, **filter_data)


@role_router.post('/', response_model=RoleBase, status_code=201)
def handle_create_role(data: RoleInput, db=Depends(get_db)):
    return RoleController().handle_create(db, data)


@role_router.get('/{uuid}', response_model=RoleResponse)
def handle_get_role(uuid: UUID, db=Depends(get_db)):
    return RoleController().handle_get(db, uuid)


@role_router.patch('/{uuid}', status_code=204)
def handle_update_role(uuid: UUID, data: RoleInput, db=Depends(get_db)):
    return RoleController().handle_patch(db, uuid, data)


@role_router.delete('/{uuid}', status_code=204)
def handle_delete_role(uuid: UUID, db=Depends(get_db)):
    return RoleController().handle_delete(db, uuid)
