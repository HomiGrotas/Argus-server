from http import HTTPStatus
from flask_restful import HTTPException


class PasswordTooShort(HTTPException):
    pass


class EmailAlreadyTaken(HTTPException):
    pass


class ChildAlreadyExists(HTTPException):
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
    "PasswordTooShort": {
        'message': 'Password is too short',
        'status': HTTPStatus.BAD_REQUEST
    },
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
    "ChildAlreadyExists":
        {
            'message': 'child mac address already exists',
            'status': HTTPStatus.BAD_REQUEST
        },
}
