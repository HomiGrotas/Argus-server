import os
import secrets
from datetime import timedelta
basedir = os.path.abspath(os.path.dirname(__file__))

EXPIRATION_MIN = 2


class Config(object):
    SECRET_KEY = """OB5TR9Ztzx3Yt9uB-eV707uJB7MCOxuH20oBO6E7pCLN4P9nIgl40tlHyYv8W6NfRh6ljt0bepeEpNnBdeFGBmTF21-knRY6dmJPf
Dwg-S2WttpwL0bZ60U0pIftxgoOCQfh6ve_rEn5kicomhjNM8wJywNiVYYWNZ6w_S2gIuFPbTiavvSkTMof6oFAoRzG4XAQV_RjrOidlGN0jWBTLan9hFtjFn15aWC7TOIsIlelNMjlXS8TpWEoPu4LDn_7QouoUMhZobmgmt7x
apNjExOG5aJPAkPyVM4RrjPk3xO2H0bGHh3medADzM_hEd-eN3UtzGUzWIKPOQXsQ5AaWg
"""
    # os.environ.get('SECRET_KEY') or secrets.token_urlsafe(256)

    #SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or \
    #                          'sqlite:///' + os.path.join(basedir, 'app.db')  # creates a local db when no uri is set

    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:my-secret-pw@localhost/db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(minutes=EXPIRATION_MIN)    # disable expiration
    DEBUG = True
