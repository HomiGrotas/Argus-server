from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity, verify_jwt_in_request
from flask import g
from typing import Union, Tuple

from .utils import valid_email, valid_mac_address, User
from app.models import Child, Parent, UsersTypes
from app.resources.exceptions import UserTypeNotSpecified
from app import auth


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


@jwt_required()
def get_user_by_jwt_token() -> Tuple[Union[Parent, Child], str]:
    """
        get users by x functions
    """
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


def get_user_by_cred(email_or_mac, password) -> Tuple[Union[Parent, Child], str]:
    if valid_email(email_or_mac):
        return get_parent_by_email_password(email_or_mac, password)

    elif valid_mac_address(email_or_mac):
        return get_child_by_mac_and_token(email_or_mac, password)


@auth.verify_password
def auth_user(email_or_mac, password) -> bool:
    """
        main auth method
    """
    user, user_type = None, None

    if verify_jwt_in_request(optional=True):
        user, user_type = get_user_by_jwt_token()
    elif email_or_mac and password:
        user, user_type = get_user_by_cred(email_or_mac, password)

    if user:
        current_user = User(user, user_type)
        g.user = current_user
        return True

    return False


@auth.get_user_roles
def user_roles(_):
    return g.user.type
