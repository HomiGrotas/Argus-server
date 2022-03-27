from flask_restful import Resource
from flask import g
from http import HTTPStatus

from .args_handlers import child_registration, child_info, child_updater
from app.resources import exceptions
from app import models, auth, db
from app.models.utils.decorators import safe_db


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

        @safe_db
        def create_child():
            db.session.add(child)
            db.session.commit()
            return {'token': child.token}, HTTPStatus.CREATED
        return create_child()

    @auth.login_required
    def get(self):
        args = child_info.parse_args()
        child_id = args.get('id')
        fields = args.get('field')

        if not child_id and g.user.type == models.UsersTypes.Child:
            child_id = g.user.user.id

        @safe_db
        def get_child():
            return models.Child.query.get(child_id)
        child = get_child()

        # get all info or info by fields
        # Security warning: Notice that key fields can be given ONLY from info function (therefore can't be manipulated)
        if child:

            # parent can see his children only
            if child.parent_id != g.user.user.id:
                raise exceptions.NotAuthorized

            info = child.info()
            if fields:
                info = {key: info[key] for key in fields if key in info}
            return info
        raise exceptions.ChildDoesntExists

    @auth.login_required(role=models.UsersTypes.Parent)
    def patch(self):
        args = child_updater.parse_args()
        child_id = args.get('id')

        @safe_db
        def get_child():
            return models.Child.query.get(child_id)
        child = get_child()

        if child:

            # parent can change his children only
            if child.parent_id != g.user.user.id:
                raise exceptions.NotAuthorized

            # update attributes
            for key, value in args.items():
                if value is not None:
                    try:
                        setattr(child, key, value)
                    except Exception as e:
                        return e.__str__(), HTTPStatus.BAD_REQUEST

            # commit in db
            @safe_db
            def update_child():
                db.session.add(child)
                db.session.commit()

            update_child()
            return child.info(), HTTPStatus.OK

        raise exceptions.ChildDoesntExists
