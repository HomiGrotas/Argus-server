from validators import email, mac_address, domain
from re import match

"""
    Customised validators
    :raises ValueError: Exception with special message in contracts to default validators functions
"""


def email_validator(supposed_email: str):
    if email(supposed_email):
        return supposed_email
    raise ValueError(f'{supposed_email} is not a valid email')


def mac_address_validator(mac: str):
    if mac_address(mac):
        return mac
    raise ValueError(f'{mac} is not a valid mac address')


def password_validator(password: str):
    return password

    # todo: password validation format
    """
    if match(r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$", password):
        return password
    raise ValueError(f'entered password is not a valid password')
    """

def domain_validator(_domain: str):
    if domain(_domain):
        return domain
    raise ValueError(f'{_domain} is not a valid domain name')
