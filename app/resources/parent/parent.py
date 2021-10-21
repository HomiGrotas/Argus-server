from flask_restful import Resource
from flask import current_app as app
from http import HTTPStatus
from flask import g

from app.resources.parent.args_handlers import parent_registration_parser, parent_updater_parser
from app.resources import exceptions
from app import models, db, auth


class Parent(Resource):
    def post(self):
        args = parent_registration_parser.parse_args()
        email = args.get('email')
        nickname = args.get('nickname')
        password = args.get('password')

        if models.Parent.query.filter_by(email=email).first() is not None:
            raise exceptions.EmailAlreadyTaken

        parent = models.Parent(email=email)
        parent.nickname = nickname
        parent.password_hash = parent.hash_password(password)

        try:
            db.session.add(parent)
            db.session.commit()
            return parent.generate_auth_token(), HTTPStatus.CREATED

        except Exception as e:
            app.logger.error("Error: %s", e.__str__())
            db.session.rollback()
            raise exceptions.InternalServerError

    @auth.login_required
    def get(self):
        if g.user_type == models.UsersTypes.parent.name:
            info = g.user.info()
        else:
            parent = Parent.query.get(g.user.parent_id)
            info = parent.info()
        return info, HTTPStatus.OK

    @auth.login_required
    def patch(self):
        if g.user_type != models.UsersTypes.parent.name:
            raise exceptions.NotAuthorized
        args = parent_updater_parser.parse_args()

        for key, value in args.items():
            if value:
                if key == 'password':
                    setattr(g.user, 'password_hash', g.user.hash_password(value))
                    continue
                if key == 'email' and value != g.user.email:
                    if models.Parent.query.filter_by(email=value).first() is not None:  # email doesn't exists
                        raise exceptions.EmailAlreadyTaken
                    setattr(g.user, key, value)
                    continue

                setattr(g.user, key, value)

        try:
            db.session.add(g.user)
            db.session.commit()

        except Exception as e:
            app.logger.error("Error: %s", e.__str__())
            db.session.rollback()
            raise exceptions.InternalServerError

        return g.user.info(), HTTPStatus.OK
