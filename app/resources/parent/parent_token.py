from flask_restful import Resource
from http import HTTPStatus
from flask import g

from app import models, auth


class ParentToken(Resource):

    @auth.login_required(role=models.UsersTypes.parent.name)
    def get(self):
        return g.user.user.generate_child_registration_token(), HTTPStatus.OK
