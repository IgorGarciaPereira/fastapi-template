from sqlalchemy import Column, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from src.database.settings import Base


class Auth(Base):
    __tablename__ = 'auth'

    email = Column(String, primary_key=True, index=True)
    password = Column(String, nullable=False)
    active = Column(Boolean, default=False)
    user_uuid = Column(String, ForeignKey('users.uuid'))
    user = relationship('User', back_populates='auth')
