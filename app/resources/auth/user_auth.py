from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from flask import g
from validators import mac_address

from app.models import Child, Parent, UsersTypes
from app.resources.exceptions import UserTypeNotSpecified
from app import auth


@jwt_required()
def get_user_by_jwt_token():
    user_type = get_jwt().get('type')
    user_id = get_jwt_identity()

    # verify token (parent/ child)
    if user_type == UsersTypes.parent.name:
        user = Parent.query.filter_by(id=user_id).first()

    elif user_type == UsersTypes.child.name:
        user = Child.query.filter_by(id=user_id).first()
    else:
        raise UserTypeNotSpecified

    return user, user_type


def get_child_by_token():
    pass


def get_parent_by_username_password():
    pass


@auth.verify_password
def auth_user(email, password):
    if email and password:
        # todo: check if username+password/ mac_address+token
        pass
    elif not password:
        g.user, g.user_type = get_user_by_jwt_token()
        return True

    return False
