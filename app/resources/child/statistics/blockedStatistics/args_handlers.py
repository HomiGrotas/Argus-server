from flask_restful import reqparse

get_parser = reqparse.RequestParser()
get_parser.add_argument('id', type=int, required=True)
