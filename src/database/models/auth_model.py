from datetime import datetime

from sqlalchemy import Column, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from src.database.settings import Base, GUID


class Auth(Base):
    __tablename__ = 'auth'

    email = Column(String, primary_key=True, index=True)
    password = Column(String, nullable=False)
    active = Column(Boolean, default=False)
    user_uuid = Column(GUID(), ForeignKey('users.uuid'))
    user = relationship('User', back_populates='auth')
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, nullable=True, default=None)
