from flask_restful import Resource
from flask import g
from http import HTTPStatus

from .args_handlers import get_blocked_parser, post_blocked_parser, delete_blocked_parser
from app.models.utils.decorators import safe_db
from app.resources import exceptions
from app import auth, models, db


class BlockedWebsites(Resource):

    @auth.login_required
    def get(self):
        args = get_blocked_parser.parse_args()
        child_id = args.get('id')

        @safe_db
        def get_child():
            return models.Child.query.get(child_id)

        child = get_child()

        if child:

            # only parent and child themself can see
            if g.user.user.id not in (child.parent_id, child.id):
                raise exceptions.NotAuthorized

            # get the activity amount specified by the user
            return child.blocked_websites, HTTPStatus.OK

        raise exceptions.ChildDoesntExists

    @auth.login_required(role=models.UsersTypes.Parent)
    def post(self):
        args = post_blocked_parser.parse_args()
        child_id = args.get('id')
        domain = args.get('domain')

        @safe_db
        def get_child():
            return models.Child.query.get(child_id)

        child = get_child()

        if child:

            # only parent can block websites to his child
            if g.user.user.id != child.parent_id:
                raise exceptions.NotAuthorized

            @safe_db
            def post_blocked_website():
                blocked_website = models.BlockedWebsites(domain=domain)
                child.blocked_websites.append(blocked_website)
                db.session.add(child)
                db.session.commit()
                return blocked_website.info(), HTTPStatus.CREATED
            return post_blocked_website()

        raise exceptions.ChildDoesntExists

    @auth.login_required(role=models.UsersTypes.Parent)
    def delete(self):
        args = delete_blocked_parser.parse_args()
        child_id = args.get('id')
        domain = args.get('domain')

        @safe_db
        def get_child():
            return models.Child.query.get(child_id)

        child = get_child()

        if child:

            # only parent can delete websites to his child
            if g.user.user.id != child.parent_id:
                raise exceptions.NotAuthorized

            @safe_db
            def delete_blocked_website():
                blocked_website = models.BlockedWebsites(domain=domain)
                db.session.add(child.blocked_websites.remove(blocked_website))
                return blocked_website.info(), HTTPStatus.CREATED
            return delete_blocked_website()

        raise exceptions.ChildDoesntExists
