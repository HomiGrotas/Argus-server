from datetime import datetime
from passlib.hash import sha256_crypt
from sqlalchemy import Column, DateTime


def hash_password(password: str) -> str:
    return sha256_crypt.hash(password)


class CreatedAt(object):
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)


class TimeStamp(object):
    start = Column(DateTime, nullable=False, default=datetime.utcnow)
    end = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
