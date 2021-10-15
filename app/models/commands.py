from sqlalchemy import Column, Integer, String, ForeignKey

from app import db
from app.models.utils import CreatedAt


class Command(CreatedAt, db.Model):
    __tablename__ = 'Commands'

    command_id = Column(Integer, primary_key=True)
    command = Column(String, nullable=False)
    to_user = Column(Integer, ForeignKey('Children.id'), nullable=False)
