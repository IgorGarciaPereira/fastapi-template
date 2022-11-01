from src.crud.base_crud import BaseCRUD
from src.database.models.auth_model import Auth


class AuthCrud(BaseCRUD):

    def __init__(self):
        super(AuthCrud, self).__init__(Auth)
