from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.controllers.base_controller import BaseController
from src.crud.role_crud import RoleCrud


class RoleController(BaseController):

    def __init__(self):
        super(RoleController, self).__init__(RoleCrud)

    def handle_delete(self, db: Session, object_id: UUID, commit=True):
        target_to_delete = self.handle_get(db, object_id)
        if target_to_delete.deletable:
            return super().handle_delete(db, object_id, commit)
        raise HTTPException(status_code=403, detail='Forbidden to delete this role')

