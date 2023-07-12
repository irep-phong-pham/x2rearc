from .error_code import ErrorCode
from src.config import Config
import i18n


class WebAPIException(Exception):
    def __init__(self, error_code: ErrorCode, message=None):
        if type(error_code) is not ErrorCode:
            raise Exception('{}: Invalid error code: {}'.format(
                ErrorCode.ERROR_CODE_NOT_FOUND,
                error_code
            ))
            
        self.message = "{}: {}".format(
            error_code.value,
            message if message is not None else i18n.t('{}.{}'.format(
                    Config.DEFAULT_ERROR_PREFIX,
                    error_code.value
                )
            )
        )
        
        self.code = error_code
        super().__init__(self.message)
