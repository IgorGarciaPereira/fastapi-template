import os
from datetime import datetime
from typing import Any, List
from sqlalchemy import update
from sqlalchemy.orm import Session
from sqlalchemy.orm.decl_api import declarative_base

from src.interfaces.base_crud_interface import BaseInterfaceCRUD
limit_default = int(os.getenv('LIMIT_LIST', 25))


class BaseCRUD(BaseInterfaceCRUD):

    def __init__(self, model: declarative_base):
        self.model = model

    def create(self, db: Session, data: Any, commit=True):
        db_object = self.model(**dict(data))
        db.add(db_object)
        if commit:
            db.commit()
            db.refresh(db_object)
        return db_object

    def get(self, db: Session, **data):
        db_customer = db.query(self.model).filter_by(**data).first()
        return db_customer

    def list(self, db: Session, skip: int = 0, limit: int = limit_default, **filter_data) -> List[Any]:
        records = db.query(self.model).filter_by(**filter_data).offset(skip).limit(limit).all()
        return records

    def patch(self, db: Session, object_id: Any, data: Any, commit=True):
        data = dict(data)
        data['updated_at'] = datetime.now()

        db.execute(
            update(self.model).where(
                self.model.uuid == object_id
            ).values(**data)
        )
        if commit:
            db.commit()
        return

    def delete(self, db: Session, object_id: Any, commit=True):
        object_instance = db.query(self.model).filter(
            self.model.uuid == object_id
        ).first()
        db.delete(object_instance)
        if commit:
            db.commit()
        return
