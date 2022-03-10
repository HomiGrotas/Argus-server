from validators import mac_address, email, ValidationFailure
from collections import namedtuple
from app.resources.exceptions import PasswordTooShort

User = namedtuple('User', ['user', 'type'])


def valid_email(user_email: str) -> bool:
    """
        custom email validator
    """
    if isinstance(email(user_email), ValidationFailure):
        return False
    else:
        return True


def valid_mac_address(user_mac_address: str) -> bool:
    """
        custom mac address validator
        user_mac_address must be a str in order to perform .replace method
    """
    if user_mac_address and not isinstance(mac_address(user_mac_address.replace('*', ':')), ValidationFailure):
        return True
    else:
        return False
