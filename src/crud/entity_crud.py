from src.crud.base_crud import BaseCRUD
from src.database.models.authorization_models import Entity


class EntityCrud(BaseCRUD):

    def __init__(self):
        super(EntityCrud, self).__init__(Entity)
