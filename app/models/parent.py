from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String
from flask_jwt_extended import create_access_token
from passlib.hash import sha256_crypt

from app import db


class Parent(db.Model):
    __tablename__ = 'Parents'

    id = Column(Integer, primary_key=True)

    email = Column(String(254), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    nickname = Column(String(32))

    children = relationship('Child')

    def verify_password(self, password):
        """ verify password. Safe from timing attacks """
        return sha256_crypt.verify(password, self.password_hash)

    def generate_child_registration_token(self):
        """ generates token for child registration """
        additional_claims = {"type": "child_registration"}
        return create_access_token(identity=self.id, additional_claims=additional_claims)

    def generate_auth_token(self):
        """ generates token for auth """
        additional_claims = {"type": "parent"}
        return create_access_token(identity=self.id, additional_claims=additional_claims)

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
    @jwt_required(locations='json')
    def get_parent_identity_by_token():
        r_type = get_jwt().get('type')
        parent_id = get_jwt_identity()
        assert r_type == 'child_registration', "Auth shouldn't go here"
        return parent_id
