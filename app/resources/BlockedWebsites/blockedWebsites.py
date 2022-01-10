from flask_restful import Resource
from http import HTTPStatus

from .args_handlers import get_blocked_parser, post_blocked_parser, delete_blocked_parser
from app.models.utils.decorators import safe_db
from app.resources import exceptions
from app import auth, models


class BlockedWebsites(Resource):

    @auth.login_required
    def get(self):
        args = get_blocked_parser.parse_args()
        child_nickname = args.get('child_nickname')
        amount = args.get('amount')

        # todo: change to block websites

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

    @auth.login_required(role=models.UsersTypes.Parent)
    def post(self):
        args = post_blocked_parser.parse_args()

    @auth.login_required(role=models.UsersTypes.Parent)
    def delete(self):
        args = delete_blocked_parser.parse_args()
