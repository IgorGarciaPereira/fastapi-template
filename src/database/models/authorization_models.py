from datetime import datetime
from sqlalchemy import Column, DateTime, String, Boolean, ForeignKey
from uuid import uuid4

from src.database.settings import Base, GUID


class Role(Base):
    __tablename__ = 'roles'

    uuid = Column(
        GUID(),
        primary_key=True,
        index=True,
        default=uuid4,
        unique=True
    )
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, nullable=True, default=None)
    name = Column(String, nullable=False, unique=True)
    deletable = Column(Boolean, default=True)


class Entity(Base):
    __tablename__ = 'entities'

    uuid = Column(
        GUID(),
        primary_key=True,
        index=True,
        default=uuid4,
        unique=True
    )
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, nullable=True, default=None)
    name = Column(String, nullable=False, unique=True)


# Association Table
class RoleEntity(Base):
    __tablename__ = 'role_entity'

    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, nullable=True, default=None)

    entity_uuid = Column(GUID(), ForeignKey('entities.uuid'), nullable=False, primary_key=True, index=True)
    role_uuid = Column(GUID(), ForeignKey('roles.uuid'), nullable=False, primary_key=True, index=True)

    can_read = Column(Boolean, default=True)
    can_write = Column(Boolean, default=False)
