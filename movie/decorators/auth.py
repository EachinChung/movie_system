from functools import wraps

from movie.models.user import User
from movie.utils.token import token_validator
from movie_system.exception import ApiError


def require_auth(func):
    @wraps(func)
    def wrapper(request, *args, **kw):
        token_type, token = request.META.get("Authorization").split(None, 1)
        if token == 'null' or token_type.lower() != 'bearer':
            raise ApiError(code='0401', message='请重新登录')

        result, token = token_validator(token)
        if not result:
            raise ApiError(code='0401', message='请重新登录')

        user_id = token['sub']
        request.user = User.objects.get_by_id(user_id)
        return func(*args, **kw)

    return wrapper
