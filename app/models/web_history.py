from sqlalchemy import Column, Integer, ForeignKey, String, DateTime

from app import db


class WebHistory(db.Model):
    __tablename__ = 'WebHistory'

    record_id = Column(Integer, primary_key=True)
    child_id = Column(Integer, ForeignKey('Children.id'),  nullable=False)
    url = Column(String, nullable=False)
    date = Column(DateTime, nullable=False)
