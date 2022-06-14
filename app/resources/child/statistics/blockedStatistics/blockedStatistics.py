from flask_restful import Resource
from flask import g
from http import HTTPStatus
from sqlalchemy import and_

from app import models, auth
from app.models.utils.decorators import safe_db
from app.resources.child.statistics.blockedStatistics.args_handlers import get_parser
from app.resources import exceptions


def get_app_statistics(child: models.Child) -> dict:
    # get amount of blocked apps compared to all apps
    count_blocked_compared_all = models.AppsHistory.query.filter(
        and_(models.AppsHistory.child_id == child.id, models.AppsHistory._blocked == 1)).count()

    # amount of apps history
    all_apps_length = len(child.apps_history)

    statistic = {
        'blocked_apps_amount': len(child.blocked_apps),
        'apps_history_length': all_apps_length,
        'blocked_amount_in_history': count_blocked_compared_all,
        'percentage':  int((count_blocked_compared_all / all_apps_length) * 100) if all_apps_length != 0 else 0,
    }
    
    return statistic


class BlockedStatistics(Resource):

    @auth.login_required(role=models.UsersTypes.Parent)
    def get(self):
        args = get_parser.parse_args()
        child_id = args.get('id')

        @safe_db
        def get_child():
            return models.Child.query.get(child_id)
        child = get_child()

        if child:
            # parent can see his children only
            # only parent and child themself can see
            if g.user.user.id != child.parent_id:
                raise exceptions.NotAuthorized

            statistic = get_app_statistics(child)

            return statistic, HTTPStatus.OK

        raise exceptions.ChildDoesntExists
