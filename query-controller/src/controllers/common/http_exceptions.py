from flask_restful import HTTPException


class WebapiHTTPException(HTTPException):
    def __init__(self, api_code=None, custom_message=None):
        super().__init__()
        self.api_code = api_code
        self.custom_message = custom_message

class HTTPBadRequestException(WebapiHTTPException):
    pass

class HTTPUnauthorizedException(WebapiHTTPException):
    pass

class HTTPPermissionDeniedException(WebapiHTTPException):
    pass

class HTTPNotFoundException(WebapiHTTPException):
    pass

class HTTPTokenExpiredException(WebapiHTTPException):
    pass

class HTTPInvalidTokenException(WebapiHTTPException):
    pass

class HTTPServerInternalException(WebapiHTTPException):
    pass

