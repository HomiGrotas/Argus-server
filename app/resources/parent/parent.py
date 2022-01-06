from flask_restful import Resource
from flask import current_app as app
from http import HTTPStatus
from flask import g

from .args_handlers import parent_registration_parser, parent_updater_parser
from app.resources import exceptions
from app import models, db, auth


class Parent(Resource):
    def post(self):
        args = parent_registration_parser.parse_args()
        email = args.get('email')
        nickname = args.get('nickname')
        password = args.get('password')

        parent = models.Parent(email=email, password_hash=models.Parent.hash_password(password), nickname=nickname)

        try:
            db.session.add(parent)
            db.session.commit()
            return parent.info(), HTTPStatus.CREATED

        except Exception as e:
            app.logger.error("Error: %s", e.__str__())
            db.session.rollback()
            raise exceptions.InternalServerError

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

        try:
            db.session.add(g.user.user)
            db.session.commit()

        except Exception as e:
            app.logger.error("Error: %s", e.__str__())
            db.session.rollback()
            raise exceptions.InternalServerError

        return g.user.user.info(), HTTPStatus.OK
