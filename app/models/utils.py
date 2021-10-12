from datetime import datetime
from passlib.hash import sha256_crypt

from app import db


def hash_password(password: str) -> str:
    return sha256_crypt.hash(password)


class CreatedAt(object):
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


class TimeStamp(object):
    start = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    end = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
