from sqlalchemy import Column, Integer, ForeignKey

from app import db
from app.models.utils import TimeStamp


class ChildActivity(db.Model, TimeStamp):
    __tablename__ = 'ChildActivity'

    id = Column(Integer, primary_key=True)
    child_id = Column(Integer, ForeignKey('Children.id'), nullable=False)

    def info(self):
        return {
                'start': self.start.__str__(),
                'end': self.end.__str__()
                }
