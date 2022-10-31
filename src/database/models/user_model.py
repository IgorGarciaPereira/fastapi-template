from datetime import datetime
from uuid import uuid4

from sqlalchemy import Column, String, DateTime

from src.database.settings import Base, GUID


class User(Base):
    __tablename__ = 'users'

    uuid = Column(
        GUID(),
        primary_key=True,
        index=True,
        default=uuid4,
        unique=True
    )
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, nullable=True)
    deleted_at = Column(DateTime, nullable=True)

    name = Column(String)
    surname = Column(String)
