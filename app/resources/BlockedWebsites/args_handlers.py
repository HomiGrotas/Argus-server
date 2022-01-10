from flask_restful import reqparse

from app.models.utils.validators import domain_validator

get_blocked_parser = reqparse.RequestParser()
get_blocked_parser.add_argument('child_nickname', type=str, required=True)
get_blocked_parser.add_argument('amount', type=int, default=10)

post_blocked_parser = reqparse.RequestParser()
post_blocked_parser.add_argument('child_id', type=int, required=True)
post_blocked_parser.add_argument('domain', type=domain_validator, required=True)

delete_blocked_parser = post_blocked_parser.copy()
