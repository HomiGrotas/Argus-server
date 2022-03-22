import os
import secrets
from datetime import timedelta
basedir = os.path.abspath(os.path.dirname(__file__))

EXPIRATION_MIN = 2


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or secrets.token_urlsafe(256)
    # SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{os.environ.get('MySQL_Username')}:{os.environ.get('MySQL_Password')}@localhost/db"
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(minutes=EXPIRATION_MIN)    # disable expiration
    DEBUG = True
    ENV = 'development'
