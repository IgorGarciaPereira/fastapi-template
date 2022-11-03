from src.crud.base_crud import BaseCRUD
from src.database.models.authorization_models import Role


class RoleCrud(BaseCRUD):
    
    def __init__(self):
        super(RoleCrud, self).__init__(Role)
