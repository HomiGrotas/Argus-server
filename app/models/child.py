from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, JSON, BOOLEAN, String, ForeignKey
from hmac import compare_digest
from secrets import token_urlsafe

from app import db


class Child(db.Model):
    __tablename__ = 'Children'

    id = Column(Integer, primary_key=True)

    parent_id = Column(Integer, ForeignKey('Parents.id'), nullable=False)
    mac_address = Column(String(17), unique=True, nullable=False)
    token = Column(String(64), nullable=False)
    nickname = Column(String(20), nullable=False)
    blocked = Column(BOOLEAN, default=False)

    usage_limits = Column(JSON)       # {day: amount}
    # block_websites = Column(String)   # MTM with blocked websites

    activity = relationship('ChildActivity')
    web_history = relationship('WebHistory')
    waiting_commands = relationship('Command')

    def verify_token(self, token):
        """ compares users token to the given one. Safe from timing attacks """
        return compare_digest(token, self.token)

    def info(self):
        return {
            'id': self.id,
            'nickname': self.nickname,
            'mac_address': self.mac_address,
        }

    @staticmethod
    def generate_token(n_bytes=64):
        """ token (64*8=) 512 bits to prevent brute-force attacks """
        return token_urlsafe(n_bytes)
