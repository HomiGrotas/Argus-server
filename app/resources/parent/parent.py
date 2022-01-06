from flask_restful import Resource
from http import HTTPStatus
from flask import g

from .args_handlers import parent_registration_parser, parent_updater_parser
from app import models, db, auth
from app.models.utils.decorators import safe_db


class Parent(Resource):
    def post(self):
        args = parent_registration_parser.parse_args()
        email = args.get('email')
        nickname = args.get('nickname')
        password = args.get('password')

        parent = models.Parent(email=email, password_hash=models.Parent.hash_password(password), nickname=nickname)

        @safe_db
        def add_child():
            db.session.add(parent)
            db.session.commit()
            return parent.info(), HTTPStatus.CREATED
        return add_child()

    @auth.login_required(role=models.UsersTypes.Parent)
    def get(self):
        return g.user.user.info(), HTTPStatus.OK

    @auth.login_required(role=models.UsersTypes.Parent)
    def patch(self):
        args = parent_updater_parser.parse_args()

        for key, value in args.items():
            if value:
                if key == 'password':
                    setattr(g.user.user, 'password_hash', g.user.user.hash_password(value))
                    continue
                setattr(g.user.user, key, value)

        @safe_db
        def update_parent():
            db.session.add(g.user.user)
            db.session.commit()

        update_parent()
        return g.user.user.info(), HTTPStatus.OK
