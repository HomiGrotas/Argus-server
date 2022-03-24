import os
import secrets
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))

EXPIRATION_MIN = 2


def get_postgres():
    uri = os.getenv("DATABASE_URL")  # or other relevant config var
    if uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)
    return uri


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or secrets.token_urlsafe(256)
    SQLALCHEMY_DATABASE_URI = get_postgres()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(minutes=EXPIRATION_MIN)    # disable expiration
    DEBUG = True
    ENV = 'development'
