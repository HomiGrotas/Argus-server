from flask_restful import Resource
from flask import render_template, make_response


class BlockedPage(Resource):
    def get(self):
        return make_response(render_template('blockedPage.html'))
