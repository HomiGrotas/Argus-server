from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from flask import g
from typing import Union, Tuple

from app.resources.auth.utils import valid_email, valid_mac_address, User
from app.models import Child, Parent, UsersTypes
from app.resources.exceptions import UserTypeNotSpecified
from app import basic_auth, token_auth

# todo: add role
# todo: change to basic jwt library


def get_parent_by_email_password(p_email: str, p_password: str) -> Tuple[Union[Parent, Child, None], Union[str, None]]:
    parent = Parent.query.filter_by(email=p_email).first()
    if parent and parent.verify_password(p_password):
        return parent, UsersTypes.parent.name
    return None, None


def get_child_by_mac_and_token(c_mac_address: str, c_token) -> Tuple[Union[Parent, Child, None], Union[str, None]]:
    child = Child.query.filter_by(mac_address=c_mac_address).first()
    if child and child.verify_token(c_token):
        return child, UsersTypes.child.name
    return None, None


@token_auth.verify_token
@jwt_required()
def get_user_by_jwt_token(token) -> bool:
    """
        get users by x functions
    """
    print('jwt <', token, '>')
    user_type = get_jwt().get('type')
    user_id = get_jwt_identity()

    # verify token (parent/ child)
    if user_type == UsersTypes.parent.name:
        user = Parent.query.filter_by(id=user_id).first()

    elif user_type == UsersTypes.child.name:
        user = Child.query.filter_by(id=user_id).first()
    else:
        raise UserTypeNotSpecified

    if user:
        current_user = User(user, user_type)
        g.user = current_user
        return True

    return False


@basic_auth.verify_password
def get_user_by_cred(email_or_mac, password) -> bool:
    print('basic <', email_or_mac, password, '>')
    user, user_type = None, None

    if valid_email(email_or_mac):
        user, user_type = get_parent_by_email_password(email_or_mac, password)

    elif valid_mac_address(email_or_mac):
        user, user_type = get_child_by_mac_and_token(email_or_mac, password)

    if user:
        current_user = User(user, user_type)
        g.user = current_user
        return True

    return False


@basic_auth.get_user_roles
def user_roles(_):
    return g.user.type


@token_auth.get_user_roles
def user_roles(_):
    return g.user.type
