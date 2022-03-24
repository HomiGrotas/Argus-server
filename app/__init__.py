from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
from flask_cors import CORS

from config import Config
from app.resources.exceptions import errors

db = SQLAlchemy()
restful = Api(errors=errors)
auth = HTTPBasicAuth()


def create_app():
    from app.resources.parent import Parent, ParentToken
    from app.resources.child import Child, ChildActivity, WebHistory
    from app.resources.commands import Commands
    from app.resources.views import BlockedPage
    from app.resources.blockedApps import BlockedApps
    from app.resources.appsHistory.appsHistory import AppsHistory
    from app.resources.blockedSites import BlockedWebsites

    app = Flask(__name__)

    @app.route('/')
    def home():
        return "working"

    @app.route('/reset')
    def reset():
        db.drop_all(app=app)
        db.create_all(app=app)
        return "reset performed"

    # load the instance config, if it exists, when not testing
    app.config.from_object(Config)

    db.init_app(app)

    # create db if doesn't exists
    if db.metadata.tables is not None:
        db.create_all(app=app)
        print("created app")

    CORS(app, resources={'*': {"origins": '*'}})

    # /parent
    restful.add_resource(Parent, '/parent')
    restful.add_resource(ParentToken, '/parent/child_registration_token')

    # /child
    restful.add_resource(Child, '/child')
    restful.add_resource(ChildActivity, '/child/activity')
    restful.add_resource(WebHistory, '/child/web_history')

    # utils
    restful.add_resource(AppsHistory, '/app_history')
    restful.add_resource(BlockedApps, '/blocked_apps')
    restful.add_resource(BlockedWebsites, '/blocked_websites')
    restful.add_resource(Commands, '/commands')
    restful.add_resource(BlockedPage, '/blocked')

    # noinspection PyTypeChecker
    restful.init_app(app)
    return app


app = create_app()


# define the shell context
@app.shell_context_processor
def shell_context():  # pragma: no cover
    from app import models

    ctx = {'db': db, 'models': models}
    return ctx

