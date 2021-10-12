from sqlalchemy.orm import relationship

from app import db


class Parent(db.Model):
    __tablename__ = 'Parents'

    id = db.Column(db.Integer, primary_key=True)

    nickname = db.Column(db.String)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(64), nullable=False)

    children = relationship('Child')
