from flask_restful import reqparse

get_commands = reqparse.RequestParser()
get_commands.add_argument('id', type=int)

post_command = get_commands.copy()
post_command.add_argument('command', type=str, required=True)

delete_command = post_command.copy()
