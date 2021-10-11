from app import db
from app.models.utils import TimeStamp


class ChildActivity(TimeStamp, db.Model):
    __tablename__ = 'ChildActivity'

    record_id = db.Column(db.Integer, primary_key=True)
    child_id = db.Column(db.Integer, db.ForeignKey('Children.id'), nullable=False)
