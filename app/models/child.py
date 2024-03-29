from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, JSON, BOOLEAN, String, ForeignKey, Enum
from sqlalchemy.orm.attributes import flag_modified
from enum import Enum as eE
from hmac import compare_digest
from secrets import token_urlsafe
from sqlalchemy.ext.hybrid import hybrid_property
from datetime import timedelta, datetime

from app import db
from app.resources import exceptions
from .utils.MTM.child_blocked_websites import child_blocked_websites
from .utils.MTM.child_blocked_apps import child_blocked_apps


class ProtectionLevels(eE):
    NO = 0
    MINIMAL = 1
    NORMAL = 2
    HARD = 3


class Child(db.Model):
    __tablename__ = 'Children'

    id = Column(Integer, primary_key=True)

    parent_id = Column(Integer, ForeignKey('Parents.id'), nullable=False)
    _mac_address = Column(String(17), unique=True, nullable=False)
    token = Column(String(154), nullable=False)
    _nickname = Column(String(20), nullable=False)
    _blocked = Column(BOOLEAN, default=False)

    _usage_limits = Column(JSON, default={
        'sunday': 1, 'monday': 1, 'tuesday': 1, 'wednesday': 1, 'thursday': 1, 'friday': 1, 'saturday': 1})       # {day: amount in hours}
    _level = Column(Enum(ProtectionLevels), nullable=False, default=ProtectionLevels.NORMAL)

    blocked_websites = relationship("BlockedWebsites", secondary=child_blocked_websites)  # MTM with blocked websites
    blocked_apps = relationship("BlockedApps", secondary=child_blocked_apps)

    apps_history = relationship("AppsHistory")
    activity = relationship('ChildActivity')
    web_history = relationship('WebHistory')
    waiting_commands = relationship('Command')

    @property
    def mac_address(self):
        return self._mac_address

    @mac_address.setter
    def mac_address(self, mac_address: str):
        # child can't have same mac address or nickname
        if Child.query.filter_by(_mac_address=mac_address).first() is not None:
            raise exceptions.ChildMacAlreadyExists
        self._mac_address = mac_address

    @property
    def nickname(self):
        return self._nickname

    @nickname.setter
    def nickname(self, nickname: str):
        # child from same parent can't have same nickname
        child_with_same_nickname = Child.query.filter(
            Child._nickname == nickname, Child.parent_id == self.parent_id).first()

        if child_with_same_nickname:
            raise exceptions.NicknameAlreadyExists
        self._nickname = nickname

    @property
    def blocked(self):
        return self._blocked

    @blocked.setter
    def blocked(self, block: bool):
        if not isinstance(block, bool):
            raise TypeError("Blocked must be boolean")
        self._blocked = block

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, new_level: int):
        if new_level is None or not 0 <= new_level <= 3:
            raise ValueError("Level must be between 0 and 4")
        self._level = ProtectionLevels(new_level)

    @property
    def usage_limits(self):
        return self._usage_limits

    @usage_limits.setter
    def usage_limits(self, new_limits: dict):
        for key, val in new_limits.items():
            try:
                val = float(val)
            except ValueError:
                raise ValueError(f"{val} is not a number!")
            if key not in self._usage_limits:
                raise KeyError(f"{key} is not an acceptable day")
            elif val < 0:
                raise ValueError(f"Hours limit must be a positive number. Got: {val}")
            self._usage_limits[key] = val
        flag_modified(self, "_usage_limits")

    @hybrid_property
    def connected(self) -> bool:
        if self.activity:
            now = datetime.utcnow()
            last = self.activity[-1].end
            return now - last < timedelta(days=1)
        return False

    @hybrid_property
    def time_spent(self) -> float:
        total = 0
        now = datetime.utcnow()
        for time in self.activity[::-1]:
            if now - time.end < timedelta(days=1):
                total += 1

        return float("{:.2f}".format(total/60))

    def verify_token(self, token):
        """ compares users token to the given one. Safe from timing attacks """
        return compare_digest(token, self.token)

    def info(self):
        return {
            'id': self.id,
            'parent_id': self.parent_id,
            'mac_address': self.mac_address,
            'nickname': self.nickname,
            'blocked': self.blocked,
            'usage_limits': self.usage_limits,
            'protection_level': self.level.value,
            'connected': self.connected,
            'time_spent': self.time_spent,
            'block_websites': 'Look at /blocked_websites',
            'activity': 'Look at /child/activity',
            'web_history': 'Look at /child/web_history',
            'waiting_commands': 'Look at /commands',
        }

    @staticmethod
    def generate_token(n_bytes=64):
        """ token (n_bytes(64)*8=) 512 bits = 154 chars to prevent brute-force attacks """
        return token_urlsafe(n_bytes)
