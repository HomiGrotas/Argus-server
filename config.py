import os
import secrets

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or secrets.token_urlsafe(256)

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or \
                              'sqlite:///' + os.path.join(basedir, 'app.db')  # creates a local db when no uri is set

    SQLALCHEMY_TRACK_MODIFICATIONS = False
