from src.controllers.base_controller import BaseController

from src.crud.role_entity_crud import RoleEntityCrud


class RoleEntityController(BaseController):
    def __init__(self):
        super(RoleEntityController, self).__init__(RoleEntityCrud)
