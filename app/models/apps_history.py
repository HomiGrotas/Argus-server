from sqlalchemy import Column, Integer, ForeignKey, String, BOOLEAN

from .utils.types import CreatedAt
from app import db


class AppsHistory(db.Model, CreatedAt):
    __tablename__ = 'AppsHistory'

    id = Column(Integer, primary_key=True)
    child_id = Column(Integer, ForeignKey('Children.id'),  nullable=False)
    _name = Column(String(2048), nullable=False)
    _blocked = Column(BOOLEAN, nullable=False)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name: str):
        self._name = new_name

    @property
    def blocked(self):
        return self._blocked

    @blocked.setter
    def blocked(self, was_blocked: bool):
        self._blocked = was_blocked
