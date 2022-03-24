import os
import secrets
from datetime import timedelta
basedir = os.path.abspath(os.path.dirname(__file__))

EXPIRATION_MIN = 2


def get_postgres():
    path = os.environ.get("DATABASE_URL")
    if not path:
        raise FileNotFoundError("Couldn't find DATABASE_URL")
    return path.replace("postgres://", "postgresql://", 1)


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or secrets.token_urlsafe(256)
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(minutes=EXPIRATION_MIN)    # disable expiration
    DEBUG = True
    ENV = 'development'
