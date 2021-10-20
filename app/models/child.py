from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, JSON, BOOLEAN, String, ForeignKey
from flask_jwt_extended import create_access_token, get_jwt_identity


from app import db


class Child(db.Model):
    __tablename__ = 'Children'

    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey('Parents.id'), nullable=False)
    nickname = Column(String, unique=True, default='Anonymous Child')
    usage_limits = Column(JSON)       # {day: amount}
    block_websites = Column(String)   # List will be parsed to '[x, y, z]'
    blocked = Column(BOOLEAN, default=False)

    activity = relationship('ChildActivity')
    web_history = relationship('WebHistory')
    waiting_commands = relationship('Command')

    def generate_auth_token(self):
        additional_claims = {"type": "child"}
        return create_access_token(identity=self.id, additional_claims=additional_claims)
