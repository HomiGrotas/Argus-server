from datetime import datetime
from sqlalchemy import Column, DateTime
from enum import Enum


class CreatedAt(object):
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)


class TimeStamp(object):
    start = Column(DateTime, nullable=False, default=datetime.utcnow)
    end = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)


class UsersTypes(Enum):
    Parent = 1
    Child = 2
