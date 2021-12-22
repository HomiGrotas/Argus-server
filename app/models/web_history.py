from sqlalchemy import Column, Integer, ForeignKey, String, BOOLEAN
from .utils.types import CreatedAt
from app import db


class WebHistory(db.Model, CreatedAt):
    __tablename__ = 'WebHistory'

    id = Column(Integer, primary_key=True)
    child_id = Column(Integer, ForeignKey('Children.id'),  nullable=False)
    url = Column(String(2048), nullable=False)
    was_blocked = Column(BOOLEAN, nullable=False)
