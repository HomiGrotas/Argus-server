from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String

from app import db


class Parent(db.Model):
    __tablename__ = 'Parents'

    id = Column(Integer, primary_key=True)

    nickname = Column(String)
    email = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(64), nullable=False)

    children = relationship('Child')
