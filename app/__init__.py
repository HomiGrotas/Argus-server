from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth

from config import Config
from app.resources.exceptions import errors

db = SQLAlchemy()
restful = Api(errors=errors)

auth = HTTPBasicAuth()  # todo: change to digest_auth


def create_app():
    from app.resources.parent import Parent, ParentToken
    from app.resources.child import Child, ChildActivity

    f_app = Flask(__name__)
    f_app.config.from_object(Config)
    db.init_app(f_app)

    restful.add_resource(Parent, '/parent')
    restful.add_resource(ParentToken, '/parent/child_registration_token')
    restful.add_resource(Child, '/child')
    restful.add_resource(ChildActivity, '/child/activity')

    # noinspection PyTypeChecker
    restful.init_app(f_app)
    return f_app


flask_app = create_app()


# define the shell context
@flask_app.shell_context_processor
def shell_context():  # pragma: no cover
    from app import models

    ctx = {'db': db, 'models': models}
    return ctx


if __name__ == '__main__':
    flask_app.run()
