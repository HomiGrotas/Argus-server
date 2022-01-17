from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth

from config import Config
from app.resources.exceptions import errors

db = SQLAlchemy()
restful = Api(errors=errors)

auth = HTTPBasicAuth()  # todo: change to digest_auth


def create_app(test_config=None):
    from app.resources.parent import Parent, ParentToken
    from app.resources.child import Child, ChildActivity, WebHistory
    from app.resources.blockedWebsites import BlockedWebsites
    from app.resources.commands import Commands
    from app.resources.views import BlockedPage

    f_app = Flask(__name__)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        f_app.config.from_object(Config)
    else:
        # load the test config if passed in
        f_app.config.update(test_config)

    db.init_app(f_app)

    # /parent
    restful.add_resource(Parent, '/parent')
    restful.add_resource(ParentToken, '/parent/child_registration_token')

    # /child
    restful.add_resource(Child, '/child')
    restful.add_resource(ChildActivity, '/child/activity')
    restful.add_resource(WebHistory, '/child/web_history')

    # utils
    restful.add_resource(BlockedWebsites, '/blocked_websites')
    restful.add_resource(Commands, '/commands')
    restful.add_resource(BlockedPage, '/blocked')

    # noinspection PyTypeChecker
    restful.init_app(f_app)
    return f_app


if __name__ == '__main__':
    flask_app = create_app()

    # define the shell context
    @flask_app.shell_context_processor
    def shell_context():  # pragma: no cover
        from app import models

        ctx = {'db': db, 'models': models}
        return ctx

    flask_app.run()
