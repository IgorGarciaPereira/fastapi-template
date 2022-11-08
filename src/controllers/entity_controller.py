from src.controllers.base_controller import BaseController
from src.crud.entity_crud import EntityCrud


class EntityController(BaseController):

    def __init__(self):
        super(EntityController, self).__init__(EntityCrud)
