from functools import wraps
from flask import current_app as app

from app import db
from app.resources import exceptions


def safe_db(func):
    """
    decorator for db functions that needs try/ except and raise InternalServerError
    :return:
    """

    @wraps(func)
    def inner():
        try:
            return func()

        except Exception as e:
            app.logger.error("Error: %s", e.__str__())
            db.session.rollback()
            raise exceptions.InternalServerError

    return inner
