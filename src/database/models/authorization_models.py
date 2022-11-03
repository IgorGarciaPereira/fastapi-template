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
    name = Column(String, nullable=False)
    deletable = Column(Boolean, default=True)


class Permission(Base):
    __tablename__ = 'permissions'

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


# Association Table
class RolePermissions(Base):
    __tablename__ = 'role_permissions'

    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, nullable=True, default=None)

    permission_uuid = Column(GUID(), ForeignKey('permissions.uuid'), nullable=False, primary_key=True, index=True)
    role_uuid = Column(GUID(), ForeignKey('roles.uuid'), nullable=False, primary_key=True, index=True)

    can_read = Column(Boolean, default=True)
    can_write = Column(Boolean, default=False)
