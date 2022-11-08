import os

from fastapi import HTTPException
from sqlalchemy.orm import Session
from typing import Any

from src.interfaces.base_controller_interface import BaseInterfaceController
limit_default = int(os.getenv('LIMIT_LIST', 25))


class BaseController(BaseInterfaceController):

    def __init__(self, crud_class: Any):
        self.crud_class = crud_class

    def handle_create(self, db: Session, data: Any, commit=True):
        return self.crud_class().create(db, data, commit)

    def handle_filter(self, db: Session, default_return=True, **data: Any):
        object_instance = self.crud_class().get(db, **data)
        if object_instance is None and default_return:
            raise HTTPException(
                status_code=404,
                detail={'message': 'resource not found'}
            )
        return object_instance

    def handle_get(self, db: Session, object_id: Any):
        object_instance = self.crud_class().get(db, uuid=object_id)
        if object_instance is None:
            raise HTTPException(
                status_code=404,
                detail={'message': 'resource not found'}
            )
        return object_instance

    def handle_list(self, db: Session, skip: int = 0, limit: int = limit_default, **filter_data):
        return self.crud_class().list(db, skip, limit, **filter_data)

    def handle_delete(self, db: Session, object_id: Any, commit=True):
        db_customer = self.crud_class().get(db, uuid=object_id)

        if db_customer is None:
            raise HTTPException(
                status_code=404,
                detail={'message': 'resource not found'}
            )

        return self.crud_class().delete(db, object_id, commit)

    def handle_patch(self, db: Session, object_id: Any, data: Any, commit=True):
        db_customer = self.crud_class().get(db, uuid=object_id)

        if db_customer is None:
            raise HTTPException(
                status_code=404,
                detail={'message': 'resource not found'}
            )

        data_dict = dict(data.__dict__)
        data_filtered = {}
        for item in data_dict.keys():
            if data_dict[item] is not None:
                data_filtered[item] = data_dict[item]

        return self.crud_class().patch(db, object_id, data_filtered, commit)
