from sqlalchemy import Column, Integer, ForeignKey, String, BOOLEAN

from .utils.types import CreatedAt
from app import db


class WebHistory(db.Model, CreatedAt):
    __tablename__ = 'WebHistory'

    id = Column(Integer, primary_key=True)
    child_id = Column(Integer, ForeignKey('Children.id'),  nullable=False)
    _url = Column(String(2048), nullable=False)
    _blocked = Column(BOOLEAN, nullable=False)

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, new_url: str):
        self._url = new_url

    @property
    def blocked(self):
        return self._blocked

    @blocked.setter
    def blocked(self, was_blocked: bool):
        self._blocked = was_blocked
