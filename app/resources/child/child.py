from flask_restful import Resource
from flask import current_app as app
from http import HTTPStatus

from .args_handlers import child_registration, child_info
from app.resources import exceptions
from app import models, auth, db


class Child(Resource):

    def post(self):
        args = child_registration.parse_args()
        mac_address = args.get('mac_address')

        # find parent by token
        parent_id = models.Parent.get_parent_identity_by_token(args.get('parent_token'))

        # create child
        nickname = args.get('nickname')
        token = models.Child.generate_token()
        child = models.Child(mac_address=mac_address, parent_id=parent_id, nickname=nickname, token=token)

        try:
            db.session.add(child)
            db.session.commit()
            return {'token': child.token}, HTTPStatus.CREATED

        except Exception as e:
            app.logger.error("Error: %s", e.__str__())
            db.session.rollback()
            raise exceptions.InternalServerError

    @auth.login_required(role=models.UsersTypes.Parent)
    def get(self):
        args = child_info.parse_args()
        child_nickname = args.get('nickname')
        fields = args.get('field')

        try:
            child = models.Child.query.filter_by(_nickname=child_nickname).first()
        except Exception as e:
            app.logger.error("Error: %s", e.__str__())
            db.session.rollback()
            raise exceptions.InternalServerError

        # get all info or info by fields
        # Security warning: Notice that key fields can be given ONLY from info function (therefore can't be manipulated)
        if child:
            info = child.info()
            if fields:
                info = {key: info[key] for key in fields if key in info}
            return info
        raise exceptions.ChildDoesntExists

    @auth.login_required(role=models.UsersTypes.Parent)
    def patch(self):
        pass

