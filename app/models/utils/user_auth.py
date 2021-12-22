from flask import g

from .auth_utils import User, valid_email, valid_mac_address
from app.models import Child, Parent, UsersTypes
from app import auth


def get_parent_by_email_password(p_email: str, p_password: str):
    parent = Parent.query.filter_by(email=p_email).first()
    if parent and parent.verify_password(p_password):
        return parent, UsersTypes.Parent
    return None, None


def get_child_by_mac_and_token(c_mac_address: str, c_token):
    child = Child.query.filter_by(mac_address=c_mac_address).first()
    if child and child.verify_token(c_token):
        return child, UsersTypes.Child
    return None, None


@auth.verify_password
def get_user_by_cred(email_or_mac, password) -> bool:
    user, user_type = None, None

    if valid_email(email_or_mac):
        user, user_type = get_parent_by_email_password(email_or_mac, password)

    elif valid_mac_address(email_or_mac):
        email_or_mac = email_or_mac.replace('*', ':')
        user, user_type = get_child_by_mac_and_token(email_or_mac, password)

    if user:
        current_user = User(user, user_type)
        g.user = current_user
        return True

    return False


@auth.get_user_roles
def user_roles(_):
    return g.user.type

