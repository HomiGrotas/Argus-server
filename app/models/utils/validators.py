from validators import email, mac_address
from re import match


def email_validator(supposed_email):
    if email(supposed_email):
        return supposed_email
    raise ValueError(f'{supposed_email} is not a valid email')


def mac_address_validator(mac):
    if mac_address(mac):
        return mac
    raise ValueError(f'{mac} is not a valid mac address')


def password_validator(password):
    if match(r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$", password):
        return password
    raise ValueError(f'entered password is not a valid password')
