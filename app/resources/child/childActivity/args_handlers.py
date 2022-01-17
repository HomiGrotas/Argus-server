from flask_restful import reqparse


get_activity_parser = reqparse.RequestParser()
get_activity_parser.add_argument('id', required=True, type=int, location='args')
get_activity_parser.add_argument('amount', type=int, location='args', default=10)
