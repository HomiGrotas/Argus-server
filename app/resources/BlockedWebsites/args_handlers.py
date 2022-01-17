from flask_restful import reqparse

from app.models.utils.validators import domain_validator

get_blocked_parser = reqparse.RequestParser()
get_blocked_parser.add_argument('id', type=int, required=True)

post_blocked_parser = get_blocked_parser.copy()
post_blocked_parser.add_argument('domain', type=domain_validator, required=True)

delete_blocked_parser = post_blocked_parser.copy()
