from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from flask import g

from app.models import Child, Parent, UsersTypes
from app.resources.exceptions import UserTypeNotSpecified
from app import auth


@jwt_required()
def get_user_by_token():
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


@auth.verify_password
def auth_user(email, password):
    if not password:
        g.user, g.user_type = get_user_by_token()
        return True
    return False
