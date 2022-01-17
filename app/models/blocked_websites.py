from sqlalchemy import Column, Integer, String, Enum
from enum import Enum as eE

from app import db


class ProtectionLevels(eE):
    NO = 0
    MINIMAL = 1
    NORMAL = 2
    HARD = 3


class BlockedWebsites(db.Model):
    __tablename__ = "BlockedWebsites"
    id = Column(Integer, primary_key=True)
    _domain = Column(String(253), nullable=False)
    _level = Column(Enum(ProtectionLevels), nullable=False, default=ProtectionLevels.NORMAL)

    @property
    def domain(self):
        return self._domain

    @domain.setter
    def domain(self, set_domain: str):
        self._domain = set_domain

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, new_level: int):
        if not 0 <= new_level <= 3:
            raise ValueError("Level must be between 0 and 4")
        self._level = ProtectionLevels(new_level)

    def info(self):
        return {
            'id': self.id,
            'domain': self.domain,
            'level': self.level.value,
        }
