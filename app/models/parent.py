from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String
from flask_jwt_extended import create_access_token
from hashlib import sha256

from app import db

# ToDo: disable tokens expiration


class Parent(db.Model):
    __tablename__ = 'Parents'

    id = Column(Integer, primary_key=True)

    email = Column(String(254), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    nickname = Column(String(32))

    children = relationship('Child')

    def hash_password(self, password):
        self.password_hash = sha256(password).hexdigest()

    def generate_auth_token(self):
        additional_claims = {"type": "parent"}
        return create_access_token(identity=self.id, additional_claims=additional_claims)

    def info(self):
        return {
            'email': self.email,
            'nickname': self.nickname
        }
