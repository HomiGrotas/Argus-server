from flask_restful import Resource
from http import HTTPStatus
from flask import g
from datetime import datetime

from app import auth, models, db
from app.models.utils.decorators import safe_db
from app.resources import exceptions
from .args_handlers import post_parser, get_parser
# validate url


class WebHistory(Resource):
    def get(self):
        pass

    @auth.login_required(role=models.UsersTypes.Child)
    def post(self):
        args = post_parser.parse_args()

        @safe_db
        def post_web_activity():
            web_activity = models.WebHistory()
            web_activity.title = args.get('title')
            web_activity.date = datetime.strptime(args.get('date'), "%Y-%m-%d %H:%M:%S")  # 2022-04-25 14:40:09
            web_activity.url = args.get('url')
            g.user.user.web_history.append(web_activity)
            db.session.add(web_activity)
            db.session.commit()
            return web_activity.info(), HTTPStatus.CREATED

        return post_web_activity()

    @auth.login_required(role=models.UsersTypes.Parent)
    def get(self):
        args = get_parser.parse_args()
        child_id = args.get('id')

        @safe_db
        def get_child():
            return models.Child.query.get(child_id)

        child = get_child()

        if child:
            # only parent can delete websites to his child
            if g.user.user.id != child.parent_id:
                raise exceptions.NotAuthorized

            return {web.id: web.info() for web in child.web_history}

        raise exceptions.ChildDoesntExists
