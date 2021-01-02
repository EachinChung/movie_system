import logging

from django.utils.deprecation import MiddlewareMixin
from pydantic.error_wrappers import ValidationError

from movie.constants.error_code import Error
from movie.utils.http_response import json_response
from movie_system.exception import ApiError

logger = logging.getLogger('django')


class MovieSystemErrMiddleware(MiddlewareMixin):
    """ 处理全局异常 """

    @staticmethod
    def process_exception(request, exception: Exception) -> json_response:
        """捕捉异常

        Args:
            request : request
            exception (Exception): 异常

        Returns:
            json_response
        """
        if isinstance(exception, ValidationError):
            # 处理 pydantic 验证错误
            err_msg = []
            for error in exception.errors():
                msg = [' -> '.join(str(e) for e in error['loc']), error["msg"]]
                err_msg.append(', '.join(msg))

            return json_response(code="FFFF", message="; ".join(err_msg))

        if isinstance(exception, ApiError):
            # 处理自定义的 api 错误
            if exception.data is None:
                exception.data = {}
            return json_response(code=exception.code, message=exception.message, data=exception.data)

        logger.exception(exception)
        code, message = Error.inter_error.unpack()
        return json_response(code=code, message=message)
