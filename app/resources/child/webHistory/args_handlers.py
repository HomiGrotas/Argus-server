from flask_restful.reqparse import RequestParser


post_parser = RequestParser()
post_parser.add_argument('url', required=True)
post_parser.add_argument('title', default='')
post_parser.add_argument('date', required=True)

get_parser = RequestParser()
get_parser.add_argument('id')
