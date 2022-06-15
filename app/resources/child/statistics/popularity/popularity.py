from flask_restful import Resource
from flask import g
from sqlalchemy import func, desc, and_

from app import models, auth, db
from app.models.utils.decorators import safe_db


class Popularity(Resource):

    @auth.login_required(role=models.UsersTypes.Parent)
    def get(self):
        children = [child.id for child in g.user.user.children]

        @safe_db
        def get_most_popular_apps():
            """ get most popular apps of the parent children"""
            return db.session.query(
                models.AppsHistory._name,
                func.count(models.AppsHistory.id).label('qty'))\
                .filter(and_(models.AppsHistory.child_id.in_(children),
                             models.AppsHistory._opened==True))\
                .group_by(models.AppsHistory._name)\
                .order_by(desc('qty')).all()

        histories = get_most_popular_apps()
        histories = [{
            'app_name': h[0],
            'amount': h[1]
        } for h in histories]

        return histories
