from src.crud.base_crud import BaseCRUD
from src.database.models.user_model import User


class UserCrud(BaseCRUD):
    def __init__(self):
        super().__init__(User)
