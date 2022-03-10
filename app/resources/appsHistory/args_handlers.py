from flask_restful import reqparse


post_handler = reqparse.RequestParser()
post_handler.add_argument('app', required=True, type=str)
post_handler.add_argument('state', choices=['closed', 'opened'], required=True)
post_handler.add_argument('blocked', type=bool, required=True)


get_handler = reqparse.RequestParser()
get_handler.add_argument('id', required=True, type=int)
get_handler.add_argument('amount', type=int, default=10)
