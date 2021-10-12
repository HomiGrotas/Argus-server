from flask_restful import Resource
from flask import current_app as app
from sqlalchemy.exc import SQLAlchemyError
from http import HTTPStatus


from app.resources.parent.args_handlers import parent_info_parser, parent_registration_parser
from app.resources import exceptions
from app.models.utils import hash_password
from app import models, db


class Parent(Resource):
    def post(self):
        args = parent_registration_parser.parse_args()
        email = args.get('email')
        password = args.get('password')
        nickname = args.get('nickname')

        if models.Parent.query.filter_by(email=email).first() is not None:
            raise exceptions.EmailAlreadyTaken

        password_hash = hash_password(password)
        parent = models.Parent(email=email, password_hash=password_hash)
        parent.nickname = nickname

        try:
            db.session.add(parent)
            db.session.commit()
            return HTTPStatus.CREATED

        except SQLAlchemyError:
            db.session.rollback()
            raise exceptions.InternalServerError

        except Exception as e:
            app.logger.error("Error: %s", e.__str__())
            raise exceptions.InternalServerError

    def get(self):
        # ToDo: tokenize with jwt (and custom info for parent/his children)

        args = parent_info_parser.parse_args()
        parent_id = args.get('id')

        parent = models.Parent.query.get(parent_id)
        if not parent:
            raise exceptions.NoSuchParent

        info = {'email': parent.email, 'nickname': parent.nickname}
        return info, HTTPStatus.OK

    def patch(self):
        # ToDo: update nickname, password and email
        pass