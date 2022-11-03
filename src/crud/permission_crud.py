from src.crud.base_crud import BaseCRUD
from src.database.models.authorization_models import Permission


class PermissionCrud(BaseCRUD):

    def __init__(self):
        super(PermissionCrud, self).__init__(Permission)
