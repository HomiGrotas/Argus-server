from flask_restful import reqparse

get_blocked_parser = reqparse.RequestParser()
get_blocked_parser.add_argument('id', type=int)

post_blocked_parser = get_blocked_parser.copy()
post_blocked_parser.add_argument('app', required=True)

delete_blocked_parser = post_blocked_parser.copy()
