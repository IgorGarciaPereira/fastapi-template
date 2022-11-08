from src.crud.base_crud import BaseCRUD
from src.database.models.authorization_models import RoleEntity


class RoleEntityCrud(BaseCRUD):
    def __init__(self):
        super(RoleEntityCrud, self).__init__(RoleEntity)
