import re

from validators import email
from flask_restful import reqparse
from re import match


def email_validator(supposed_email):
    if email(supposed_email):
        return supposed_email
    raise ValueError(f'{supposed_email} is not a valid email')


def password_validator(password):
    if match(r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$", password):
        return password
    raise ValueError(f'entered password is not a valid password')


parent_registration_parser = reqparse.RequestParser()
parent_registration_parser.add_argument('email', required=True, type=email_validator, location='json')
parent_registration_parser.add_argument('password', required=True, type=password_validator, location='json')
parent_registration_parser.add_argument('nickname', type=str, location='json')


parent_info_parser = reqparse.RequestParser()
parent_info_parser.add_argument('id', required=True, location='args')
