from jwt import encode, decode, ExpiredSignatureError, InvalidTokenError
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String
from passlib.hash import sha256_crypt
from flask import current_app
from time import time

from app import db
from app.resources import exceptions


class Parent(db.Model):
    __tablename__ = 'Parents'

    id = Column(Integer, primary_key=True)

    _email = Column(String(254), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    _nickname = Column(String(32), unique=True, nullable=False)

    children = relationship('Child')

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, email: str):
        if Parent.query.filter_by(_email=email).first() is not None:  # ensure email doesn't exists
            raise exceptions.EmailAlreadyTaken
        self._email = email

    @property
    def nickname(self):
        return self._nickname

    @nickname.setter
    def nickname(self, nickname: str):
        if Parent.query.filter_by(_nickname=nickname).first() is not None:  # ensure nickname doesn't exists
            raise exceptions.NicknameAlreadyExists
        self._nickname = nickname

    def verify_password(self, password):
        """ verify password. Safe from timing attacks """
        return sha256_crypt.verify(password, self.password_hash)

    def generate_child_registration_token(self, time_delta=300):
        """ generates token for child registration """
        return encode(
            {'id': self.id, 'exp': time() + time_delta},
            current_app.config.get('SECRET_KEY'),
            algorithm='HS256'
        )

    def info(self):
        return {
            'id': self.id,
            'email': self.email,
            'nickname': self.nickname,
            'children': [child.info() for child in self.children],
        }

    @staticmethod
    def hash_password(password):
        return sha256_crypt.hash(password)

    @staticmethod
    def get_parent_identity_by_token(auth_token):
        """
         Decodes the auth token
         :param auth_token:
         :return: integer|string
         """
        try:
            payload = decode(auth_token, current_app.config.get('SECRET_KEY'), algorithms='HS256')
            parent_id = payload.get('id')

        except ExpiredSignatureError:
            raise exceptions.TokenExpired
        except InvalidTokenError:
            raise exceptions.InvalidSignatureError
        return parent_id
