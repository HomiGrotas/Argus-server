from validators import mac_address, email, ValidationFailure
from collections import namedtuple

# todo: move to models

User = namedtuple('User', ['user', 'type'])


def valid_email(user_email: str) -> bool:
    """
        custom email validator
    """
    try:
        email(user_email)
    except ValidationFailure:
        return False
    else:
        return True


def valid_mac_address(user_mac_address: str) -> bool:
    """
        custom mac address validator
    """
    try:
        mac_address(user_mac_address)
    except ValidationFailure:
        return False
    else:
        return True
