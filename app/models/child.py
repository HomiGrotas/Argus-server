from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, JSON, BOOLEAN, String, ForeignKey
from hmac import compare_digest
from secrets import token_urlsafe
from sqlalchemy.ext.hybrid import hybrid_property

from app import db
from app.resources import exceptions
from .utils.MTM.child_blocked_websites import child_blocked_websites


class Child(db.Model):
    __tablename__ = 'Children'

    id = Column(Integer, primary_key=True)

    parent_id = Column(Integer, ForeignKey('Parents.id'), nullable=False)
    _mac_address = Column(String(17), unique=True, nullable=False)
    token = Column(String(154), nullable=False)
    _nickname = Column(String(20), nullable=False, unique=True)
    blocked = Column(BOOLEAN, default=False)

    usage_limits = Column(JSON)       # {day: amount}

    block_websites = relationship("BlockedWebsites", secondary=child_blocked_websites)  # MTM with blocked websites
    activity = relationship('ChildActivity')
    web_history = relationship('WebHistory')
    waiting_commands = relationship('Command')

    @hybrid_property
    def mac_address(self):
        return self._mac_address

    @mac_address.setter
    def mac_address(self, mac_address):
        # child can't have same mac address or nickname
        if Child.query.filter_by(mac_address=mac_address).first() is not None:
            raise exceptions.ChildAlreadyExists

        self._mac_address = mac_address

    @hybrid_property
    def nickname(self):
        return self._nickname

    @nickname.setter
    def nickname(self, nickname: str):
        # child can't have same mac address or nickname
        if Child.query.filter_by(_nickname=nickname).first() is not None:
            raise exceptions.ChildAlreadyExists
        self._nickname = nickname

    def verify_token(self, token):
        """ compares users token to the given one. Safe from timing attacks """
        return compare_digest(token, self.token)

    def info(self):
        return {
            'id': self.id,
            'nickname': self._nickname,
            'mac_address': self._mac_address,
        }

    @staticmethod
    def generate_token(n_bytes=64):
        """ token (n_bytes(64)*8=) 512 bits = 154 chars to prevent brute-force attacks """
        return token_urlsafe(n_bytes)
