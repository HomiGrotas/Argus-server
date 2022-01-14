from flask_restful import reqparse

get_commands = reqparse.RequestParser()
get_commands.add_argument('nickname')

post_command = get_commands.copy()
post_command.add_argument('command')

delete_command = post_command.copy()
