from sqlalchemy import Column , Integer
from sqlalchemy.orm import declarative_base, relationship
from ..base import Base
from .dictionary import Dictionary


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True)
    dictionary = relationship("Dictionary")