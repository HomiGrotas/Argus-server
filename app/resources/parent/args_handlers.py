from flask_restful import reqparse
from app.models.utils.validators import email_validator, password_validator


parent_registration_parser = reqparse.RequestParser(bundle_errors=True)
parent_registration_parser.add_argument('email', required=True, type=email_validator, location='json')
parent_registration_parser.add_argument('password', required=True, type=password_validator, location='json')
parent_registration_parser.add_argument('nickname', required=True, type=str, location='json')

parent_updater_parser = reqparse.RequestParser(bundle_errors=True)
parent_updater_parser.add_argument('email', type=email_validator, location='json')
parent_updater_parser.add_argument('password', type=password_validator, location='json')
parent_updater_parser.add_argument('nickname', type=str, location='json')
