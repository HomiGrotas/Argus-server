from flask_restful import Resource
from flask import g
from http import HTTPStatus

from .args_handlers import get_activity_parser
from app import auth, models, db
from app.models.utils.decorators import safe_db
from app.resources import exceptions


class ChildActivity(Resource):
    @auth.login_required(role=models.UsersTypes.Child)
    def post(self):

        activity = models.ChildActivity()
        activity.child_id = g.user.user.id

        @safe_db
        def add_activity():
            db.session.add(activity)
            db.session.commit()
            return {'activity': activity.info()}, HTTPStatus.CREATED
        return add_activity()

    @auth.login_required(role=models.UsersTypes.Parent)
    def get(self):
        args = get_activity_parser.parse_args()
        child_nickname = args.get('nickname')
        amount = args.get('amount')

        @safe_db
        def get_child():
            return models.Child.query.filter_by(_nickname=child_nickname).first()

        child = get_child()

        if child:
            # parent can see his children only
            if child.parent_id != g.user.user.id:
                raise exceptions.NotAuthorized

            # get the activity amount specified by the user
            return [child.activity[i].info() for i in range(amount)], HTTPStatus.OK

        raise exceptions.ChildDoesntExists
