from flask_restful import reqparse

from app.models.utils.validators import mac_address_validator


child_registration = reqparse.RequestParser()
child_registration.add_argument('mac_address', required=True, type=mac_address_validator, location='json')
child_registration.add_argument('nickname', required=True, type=str, location='json')
child_registration.add_argument('parent_token', required=True, location='json')  # JWT token for attaching to parent

child_info = reqparse.RequestParser()
child_info.add_argument('id', required=True, type=int, location='args')
child_info.add_argument('field', type=str, location='args', action='append')

child_updater = reqparse.RequestParser()
child_updater.add_argument('id', type=int, required=True, location='args')
child_updater.add_argument('nickname', type=str, location='json')
child_updater.add_argument('blocked', type=bool, location='json')
