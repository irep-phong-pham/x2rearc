import jwt
import traceback
from functools import wraps
from collections import namedtuple

from flask import request
import flask_restful
from webargs import ValidationError
from webargs.flaskparser import parser

from src.controllers.common import http_exceptions
from src.exceptions import WebAPIException, ErrorCode


@parser.error_handler
def handle_error(error, req, schema, *, error_status_code, error_headers):
    raise error


def token_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            UserSession = namedtuple('UserSession',['email', 'cognito_id'])

            auth_headers = request.headers.get('Authorization', '').split()
            if len(auth_headers) == 1:
                raise http_exceptions.HTTPUnauthorizedException
            elif len(auth_headers) != 2:
                raise http_exceptions.HTTPInvalidTokenException

            token = auth_headers[1]
            data = jwt.decode(token, options={"verify_signature": False})

            cognito_id = data['sub']
            email = data['email']

            current_user = UserSession(email=email, cognito_id=cognito_id)
            return func(current_user, *args, **kwargs)
        except jwt.DecodeError as e:
            traceback.print_exc()
            raise http_exceptions.HTTPServerInternalException(
                custom_message=(str(e)))
        except jwt.ExpiredSignatureError as e:
            raise http_exceptions.HTTPTokenExpiredException
        except jwt.InvalidTokenError as e:
            raise http_exceptions.HTTPInvalidTokenException
        except ValidationError as ve:
            traceback.print_exc()
            raise http_exceptions.HTTPBadRequestException(
                custom_message=str(ve))
        except WebAPIException as e:
            traceback.print_exc()
            raise http_exceptions.HTTPServerInternalException(
                custom_message=(str(e)))
        except Exception as e:
            traceback.print_exc()
            raise http_exceptions.HTTPServerInternalException
        finally:
            pass

    return wrapper


class BaseController(flask_restful.Resource):
    def __init__(self, *args, **kwargs):
        super().__init__()

    method_decorators = [token_required]
