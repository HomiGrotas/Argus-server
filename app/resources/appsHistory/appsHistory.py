from flask_restful import Resource
from flask import g
from http import HTTPStatus

from .args_handlers import post_handler, get_handler
from app.models.utils.decorators import safe_db
from app.resources import exceptions
from app import auth, models, db


class AppsHistory(Resource):

    @staticmethod
    @auth.login_required(role=models.UsersTypes.Parent)
    def get():
        args = get_handler.parse_args()
        child_id = args.get('id')
        amount = args.get('amount')

        @safe_db
        def get_child():
            return models.Child.query.get(child_id)

        child = get_child()

        if child:

            # only the child parent can view
            if g.user.user.id != child.parent_id:
                raise exceptions.NotAuthorized

            # get the activity amount specified by the user
            history_length = len(child.apps_history)
            if amount < history_length:
                status = HTTPStatus.PARTIAL_CONTENT
            else:
                amount = history_length
                status = HTTPStatus.OK
            return [child.apps_history[i].info() for i in range(amount)], status

        raise exceptions.ChildDoesntExists

    @staticmethod
    @auth.login_required(role=models.UsersTypes.Child)
    def post():
        args = post_handler.parse_args()
        app = args.get('app')
        state = args.get('state')
        blocked = args.get('blocked')

        @safe_db
        def add_history():
            history = models.AppsHistory()
            history.name = app
            history.blocked = blocked
            history.state = state
            g.user.user.apps_history.append(history)
            db.session.add(g.user.user)
            db.session.commit()
            return history.info(), HTTPStatus.CREATED
        return add_history()
