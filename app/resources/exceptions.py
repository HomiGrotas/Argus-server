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


class TokenExpired(HTTPException):
    pass


class UserTypeNotSpecified(HTTPException):
    pass


class ChildDoesntExists(HTTPException):
    pass


class NotAuthorized(HTTPException):
    pass


class NicknameAlreadyExists(HTTPException):
    pass


class ChildMacAlreadyExists(HTTPException):
    pass


class DomainDoesntExists(HTTPException):
    pass


class DomainAlreadyExists(HTTPException):
    pass


errors = {
    "ChildMacAlreadyExists":
        {
            'message': "Child mac address already exists",
            'status': HTTPStatus.BAD_REQUEST
        },
    "NicknameAlreadyExists":
        {
            'message': "Chosen nickname already exists",
            'status': HTTPStatus.BAD_REQUEST
        },
    "ChildDoesntExists":
        {
            'message': "Child doesn't exists",
            'status': HTTPStatus.NOT_FOUND
        },
    "PasswordTooShort":
        {
            'message': 'Password is too short',
            'status': HTTPStatus.BAD_REQUEST
        },
    'EmailAlreadyTaken':
        {
            'message': 'email is already taken',
            'status': HTTPStatus.BAD_REQUEST
        },

    "InternalServerError":
        {
            'message': "Oops! Internal error occurred",
            'status': HTTPStatus.INTERNAL_SERVER_ERROR
        },

    "NoSuchParent":
        {
            'message': "No such parent",
            'status': HTTPStatus.NOT_FOUND
        },

    "TokenExpired":
        {
            'message': "The given token is expired. Please request your parent for a new token",
            'status': HTTPStatus.NOT_ACCEPTABLE
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
    "DomainDoesntExists":
        {
            'message': "specified domain doesn't exists",
            'status': HTTPStatus.NOT_FOUND
        },
    "DomainAlreadyExists":
        {
            'message': "specified domain already exists",
            'status': HTTPStatus.BAD_REQUEST
        },
}
