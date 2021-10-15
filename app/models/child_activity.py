from sqlalchemy import Column, Integer, ForeignKey

from app import db
from app.models.utils import TimeStamp


class ChildActivity(TimeStamp, db.Model):
    __tablename__ = 'ChildActivity'

    record_id = Column(Integer, primary_key=True)
    child_id = Column(Integer, ForeignKey('Children.id'), nullable=False)
