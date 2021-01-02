from functools import wraps

from django.core.handlers.wsgi import WSGIRequest

from movie.models.user import User
from movie.utils.token import token_validator
from movie_system.exception import ApiError


def require_auth(func):
    @wraps(func)
    def wrapper(api_obj, request: WSGIRequest, *args, **kw):
        try:
            token_type, token = request.META.get("HTTP_AUTHORIZATION").split(None, 1)
        except ValueError:
            raise ApiError(code='0401', message='请重新登录')

        if token == 'null' or token_type.lower() != 'bearer':
            raise ApiError(code='0401', message='请重新登录')

        result, token = token_validator(token)
        if not result:
            raise ApiError(code='0401', message='请重新登录')

        user_id = token['sub']
        request.user = User.objects.get_by_id(user_id)
        return func(api_obj, request, *args, **kw)

    return wrapper
