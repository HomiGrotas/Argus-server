from flask_restful import reqparse

from app.resources.utils import mac_address_validator


child_registration = reqparse.RequestParser()
child_registration.add_argument('mac_address', required=True, type=mac_address_validator, location='json')
child_registration.add_argument('nickname', required=True, type=str, location='json')
child_registration.add_argument('access_token', required=True, location='json')  # JWT token for attaching to parent
