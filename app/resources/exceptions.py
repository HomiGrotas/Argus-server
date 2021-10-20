from http import HTTPStatus

# noinspection PyProtectedMember
from flask_restful import HTTPException


class EmailAlreadyTaken(HTTPException):
    pass


class InternalServerError(HTTPException):
    pass


class NoSuchParent(HTTPException):
    pass


class NoAuthorizationError(HTTPException):
    pass


class InvalidSignatureError(HTTPException):
    pass


class UserTypeNotSpecified(HTTPException):
    pass


class NotAuthorized(HTTPException):
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

    "NoAuthorizationError":
        {
            'message': "Missing Authorization Header",
            'status': HTTPStatus.NOT_ACCEPTABLE
        },
    "InvalidSignatureError":
        {
            'message': "Token verification failed",
            'status': HTTPStatus.UNAUTHORIZED
        },
    "UserTypeNotSpecified":
        {
            'message': "user type is needed for further auth",
            'status': HTTPStatus.NOT_ACCEPTABLE
        },
    "NotAuthorized":
        {
            'message': "you aren't authorized for this method",
            'status': HTTPStatus.UNAUTHORIZED
        },
}