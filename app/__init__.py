from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_httpauth import HTTPBasicAuth

from config import Config
from app.resources.exceptions import errors

db = SQLAlchemy()
restful = Api(errors=errors)
jwt = JWTManager()
auth = HTTPBasicAuth()


def create_app():
    from app.resources.parent import Parent

    f_app = Flask(__name__)
    f_app.config.from_object(Config)
    db.init_app(f_app)

    if f_app.debug:
        db.create_all(app=f_app)
        print(" * Reset db: flask_app is in debug mode")

    restful.add_resource(Parent, '/parent')

    # noinspection PyTypeChecker
    restful.init_app(f_app)
    jwt.init_app(f_app)
    return f_app


if __name__ == '__main__':
    flask_app = create_app()
    flask_app.run()
