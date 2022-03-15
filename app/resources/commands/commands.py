from flask_restful import Resource
from flask import g
from http import HTTPStatus

from app.models.utils.decorators import safe_db
from app import models, auth, db
from app.resources import exceptions
from .args_handlers import get_commands, post_command, delete_command


class Commands(Resource):

    @auth.login_required
    def get(self):
        args = get_commands.parse_args()
        child_id = args.get('id')

        if not child_id and g.user.type == models.UsersTypes.Child:
            child_id = g.user.user.id

        @safe_db
        def get_child():
            return models.Child.query.get(child_id)

        child = get_child()
        if child:
            if g.user.user.id not in (child.parent_id, child.id):
                raise exceptions.NotAuthorized
            return {command.id: command.info() for command in child.waiting_commands}

        raise exceptions.ChildDoesntExists

    @auth.login_required(role=models.UsersTypes.Parent)
    def post(self):
        args = post_command.parse_args()
        child_id = args.get('id')
        command = args.get('command')

        @safe_db
        def get_child():
            return models.Child.query.get(child_id)

        child = get_child()
        if child:
            if g.user.user.id != child.parent_id:
                raise exceptions.NotAuthorized

            @safe_db
            def add_command():
                cmd = models.Command()
                cmd.command = command
                cmd.to_user = child_id
                child.waiting_commands.append(cmd)
                db.session.add(child)
                db.session.commit()
                return cmd.info(), HTTPStatus.CREATED
            return add_command()

        raise exceptions.ChildDoesntExists

    def delete(self):
        pass
