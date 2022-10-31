from src.controllers.base_controller import BaseController
from src.crud.user_crud import UserCrud


class UserController(BaseController):

    def __init__(self):
        super(UserController, self).__init__(crud_class=UserCrud)
