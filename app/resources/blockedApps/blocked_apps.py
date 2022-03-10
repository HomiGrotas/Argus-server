from flask_restful import Resource
from flask import g
from http import HTTPStatus

from .args_handlers import get_blocked_parser, post_blocked_parser, delete_blocked_parser
from app.models.utils.decorators import safe_db
from app.resources import exceptions
from app import auth, models, db


class BlockedApps(Resource):

    @auth.login_required
    def get(self):
        args = get_blocked_parser.parse_args()
        child_id = args.get('id')

        if not child_id and g.user.type == models.UsersTypes.Child:
            child_id = g.user.user.id

        @safe_db
        def get_child():
            return models.Child.query.get(child_id)

        child = get_child()

        if child:

            # only parent and child themself can see
            if g.user.user.id not in (child.parent_id, child.id):
                raise exceptions.NotAuthorized

            # get the activity amount specified by the user
            return [b.info() for b in child.blocked_apps], HTTPStatus.OK

        raise exceptions.ChildDoesntExists

    @auth.login_required(role=models.UsersTypes.Parent)
    def post(self):
        args = post_blocked_parser.parse_args()
        child_id = args.get('id')
        app = args.get('app')

        @safe_db
        def get_child():
            return models.Child.query.get(child_id)

        child = get_child()

        if child:

            # only parent can block websites to his child
            if g.user.user.id != child.parent_id:
                raise exceptions.NotAuthorized

            app_exists = tuple(filter(lambda s: s.app == app, child.blocked_apps))  # search specified app
            if app_exists:
                raise exceptions.DomainAlreadyExists

            @safe_db
            def post_blocked_website():
                blocked_app = models.BlockedApps()
                blocked_app.app = app
                child.blocked_apps.append(blocked_app)
                db.session.add(child)
                db.session.commit()
                return blocked_app.info(), HTTPStatus.CREATED
            return post_blocked_website()

        raise exceptions.ChildDoesntExists

    @auth.login_required(role=models.UsersTypes.Parent)
    def delete(self):
        args = delete_blocked_parser.parse_args()
        child_id = args.get('id')
        app = args.get('app')

        @safe_db
        def get_child():
            return models.Child.query.get(child_id)

        child = get_child()

        if child:

            # only parent can delete websites to his child
            if g.user.user.id != child.parent_id:
                raise exceptions.NotAuthorized

            app = tuple(filter(lambda s: s.app == app, child.blocked_apps))  # search specified app
            if not app:
                raise exceptions.DomainDoesntExists

            @safe_db
            def delete_blocked_website():
                child.blocked_apps.remove(app[0])     # there should be only one site
                db.session.add(child)
                db.session.commit()
                return [b.info() for b in child.blocked_apps], HTTPStatus.OK
            return delete_blocked_website()

        raise exceptions.ChildDoesntExists
