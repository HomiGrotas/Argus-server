from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
from flask_cors import CORS
from dotenv import load_dotenv
load_dotenv()

from config import Config
from app.resources.exceptions import errors

db = SQLAlchemy()
restful = Api(errors=errors)
auth = HTTPBasicAuth()


def create_app(test_config=None):
    from app.resources.parent import Parent, ParentToken
    from app.resources.child import Child, ChildActivity, WebHistory
    #from app.resources.blockedWebsites import BlockedWebsites
    from app.resources.commands import Commands
    from app.resources.views import BlockedPage
    from app.resources.blockedApps import BlockedApps
    from app.resources.appsHistory.appsHistory import AppsHistory

    app = Flask(__name__)

    @app.route('/')
    def home():
        return "working"

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_object(Config)
    else:
        # load the test config if passed in
        app.config.update(test_config)

    db.init_app(app)
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
    #restful.add_resource(BlockedWebsites, '/blocked_websites')
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

