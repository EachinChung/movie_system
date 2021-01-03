from functools import wraps

from asgiref.sync import sync_to_async

from movie.models.user import User
from movie.utils.token import get_user_id_by_token


def require_auth(func):
    """ 限制登录才能访问 """
    @wraps(func)
    def wrapper(api_obj, request, *args, **kw):
        user_id = get_user_id_by_token(request)
        request.user = User.objects.get_by_id(user_id)
        return func(api_obj, request, *args, **kw)

    return wrapper


def require_auth_async(func):
    """ 限制登录才能访问 """
    @wraps(func)
    async def wrapper(api_obj, request, *args, **kw):
        user_id = get_user_id_by_token(request)
        request.user = await sync_to_async(User.objects.get_by_id, thread_sensitive=True)(user_id)
        return await func(api_obj, request, *args, **kw)

    return wrapper
