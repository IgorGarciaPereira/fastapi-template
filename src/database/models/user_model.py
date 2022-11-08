from datetime import datetime
from uuid import uuid4

from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

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
    updated_at = Column(DateTime, nullable=True, default=None)

    name = Column(String, nullable=True)
    surname = Column(String, nullable=True)
    auth = relationship('Auth', back_populates='user', cascade='all, delete-orphan')
    role_uuid = Column(GUID(), ForeignKey('roles.uuid'), nullable=True)
