from typing import Any
from sqlalchemy import Column , Integer, String, ForeignKey
from sqlalchemy.orm import relationship 
from ..base import Base


class Word(Base):
    __tablename__ = 'word'

    id = Column(Integer, primary_key=True)
    dict_id = Column(Integer, ForeignKey("dictionary.id"))
    language: str = Column(String)
    origin: str = Column(String)
    translate: str = Column(String)

    def get_as_dict(self) -> dict:
        return {
            'id': self.id, 
            'dict_id': self.dict_id, 
            'language': self.language, 
            'origin': self.origin, 
            'translate': self.translate
            }


class Dictionary(Base):
    __tablename__ = 'dictionary'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))

    title: str = Column(String)
    language_src: str  = Column(String)
    language_dist: str = Column(String)
    words: list[Word] = relationship("Word")

    def get_as_dict(self) -> dict:
        return {
            'id': self.id, 
            'user_id': self.user_id, 
            'title': self.title, 
            'language_src': self.language_src, 
            'language_dist': self.language_dist,
            'words': [ word.get_as_dict() for word in self.words]
            }
