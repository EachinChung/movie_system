from functools import wraps

from django.core.cache import cache

from movie_system.exception import ApiError


def call_second_limit_async(second):
    def decorator(func):
        @wraps(func)
        async def wrapped_view(api_obj, request, *args, **kwargs):
            key = f"second:limit:{api_obj.__class__.__name__}:{func.__name__}:{request.user.id}"
            result = cache.get(key)
            if result:
                raise ApiError(code='0204', message='请稍后再试')

            cache.set(key, 'limit', timeout=second)
            return await func(api_obj, request, *args, **kwargs)

        return wrapped_view

    return decorator
