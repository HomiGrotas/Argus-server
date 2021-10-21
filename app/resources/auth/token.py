from flask_restful import Resource
from flask import g

from app import auth


class Token(Resource):

    @auth.login_required
    def get(self):
        return g.user.generate_auth_token()
