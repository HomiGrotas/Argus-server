from sqlalchemy import Column, Integer, String, ForeignKey

from app import db
from app.models.utils import CreatedAt


class Command(db.Model, CreatedAt):
    __tablename__ = 'Commands'

    id = Column(Integer, primary_key=True)
    command = Column(String(50), nullable=False)
    to_user = Column(Integer, ForeignKey('Children.id'), nullable=False)
