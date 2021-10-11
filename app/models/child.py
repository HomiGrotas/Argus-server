from sqlalchemy.orm import relationship

from app import db


class Child(db.Model):
    __tablename__ = 'Children'

    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('Parents.id'), nullable=False)
    nickname = db.Column(db.String, unique=True, default='Anonymous Child')
    usage_limits = db.Column(db.JSON)
    block_websites = db.Column(db.String)   # List will be parsed to '[x, y, z]'
    activity = relationship('ChildActivity')
    web_history = relationship('WebHistory')
    waiting_commands = relationship('Commands')
    blocked = db.Column(db.BOOLEAN, default=False)
