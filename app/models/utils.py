from datetime import datetime

from app import db


class CreatedAt(object):
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


class TimeStamp(object):
    start = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    end = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
