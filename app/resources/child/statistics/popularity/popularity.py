from flask_restful import Resource
from flask import g
from sqlalchemy import func, desc

from app.resources import exceptions
from app import models, auth, db
from app.models.utils.decorators import safe_db


class Popularity(Resource):

    @auth.login_required(role=models.UsersTypes.Parent)
    def get(self):
        children = [child.id for child in g.user.user.children]

        # get most popular apps of the parent children
        histories = db.session.query(
            models.AppsHistory._name,
            func.count(models.AppsHistory.id).label('qty'))\
            .filter(models.AppsHistory.child_id.in_(children))\
            .group_by(models.AppsHistory._name)\
            .order_by(desc('qty')).all()

        histories = [{
            'app_name': h[0],
            'amount': h[1]
        }
            for h in histories]
        return histories
