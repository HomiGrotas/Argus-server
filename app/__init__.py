from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

from config import Config
from app.resources.exceptions import errors

db = SQLAlchemy()
restful = Api(errors=errors)


def create_app():
    from app.resources.parent import Parent

    flask_app = Flask(__name__)
    flask_app.config.from_object(Config)
    db.init_app(flask_app)

    if flask_app.debug:
        db.create_all(app=flask_app)
        print(" * Reset db: flask_app is in debug mode")

    restful.add_resource(Parent, '/parent')

    # noinspection PyTypeChecker
    restful.init_app(flask_app)
    return flask_app


flask_app = create_app()
