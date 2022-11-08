from fastapi import APIRouter, Depends
from typing import List

from src.controllers.entity_controller import EntityController
from src.database.settings import get_db
from src.middleware import is_authenticated, IsAuthorized
from src.schemas.entity_schema import EntityCreated, Entity, EntityInput


is_authorized = IsAuthorized(entity='entities')

entity_router = APIRouter(
    prefix='/entity',
    tags=['Entity'],
    dependencies=[Depends(is_authenticated), Depends(is_authorized)]
)


@entity_router.get('/', response_model=List[Entity])
def get_list_permissions(db=Depends(get_db)):
    """
    Return all permission.
    """
    return EntityController().handle_list(db)


@entity_router.get('/{uuid}', response_model=Entity)
def get_specific_permission(uuid: str, db=Depends(get_db)):
    """
    Return a specific permission by UUID.
    """
    return EntityController().handle_get(db, object_id=uuid)


@entity_router.post('/', status_code=201, response_model=EntityCreated)
def create_permission(data: EntityInput, db=Depends(get_db)):
    """
    Create a new permission.
    """
    return EntityController().handle_create(db, data)


@entity_router.patch('/{uuid}', status_code=204)
def update_permission(uuid: str, data: EntityInput, db=Depends(get_db)):
    return EntityController().handle_patch(db, uuid, data)


@entity_router.delete('/{uuid}', status_code=204)
def delete_permission(uuid: str, db=Depends(get_db)):
    """
    Delete a specific permission
    """
    return EntityController().handle_delete(db, uuid)
