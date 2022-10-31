from sqlalchemy import Column, String, DateTime

from uuid import uuid4

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
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)

    name = Column(String)
    surname = Column(String)
