from datetime import datetime

from sqlalchemy import update
from sqlalchemy.orm import Session
from typing import Any

from src.crud.base_crud import BaseCRUD
from src.database.models.auth_model import Auth


class AuthCrud(BaseCRUD):

    def __init__(self):
        super(AuthCrud, self).__init__(Auth)

    def patch(self, db: Session, email: str, data: Any, commit=True):
        data = dict(data)
        data['updated_at'] = datetime.now()

        db.execute(
            update(self.model).where(
                self.model.email == email
            ).values(**data)
        )
        if commit:
            db.commit()
        return
