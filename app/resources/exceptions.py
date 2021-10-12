from http import HTTPStatus

# noinspection PyProtectedMember
from flask_restful import HTTPException


class EmailAlreadyTaken(HTTPException):
    pass


class InternalServerError(HTTPException):
    pass


class NoSuchParent(HTTPException):
    pass


errors = {

    'EmailAlreadyTaken': {
        'message': 'email is already taken',
        'status': HTTPStatus.BAD_REQUEST
    },

    "InternalServerError": {
        'message': "Oops! Internal error occurred",
        'status': HTTPStatus.INTERNAL_SERVER_ERROR
    },

    "NoSuchParent":
        {
            'message': "No such parent",
            'status': HTTPStatus.NOT_FOUND
        },
}