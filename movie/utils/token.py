import datetime
from typing import Tuple, Union

import jwt

from movie_system import settings
from movie_system.exception import ApiError


def create_token(sub: str, data: dict = None, exp: int = 60, secret: str = settings.SECRET_KEY) -> str:
    """创建token

    Args:
        sub (str): 签发给谁
        data (dict, optional): token内容. Defaults to None.
        exp (int, optional): 多久分钟后过期. Defaults to 60.
        secret (str, optional): 秘钥. Defaults to settings.SECRET_KEY.

    Returns:
        str: token
    """
    payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=exp),
        'iat': datetime.datetime.utcnow(),
        'sub': sub
    }

    if data is not None:
        payload.update(data)

    signature = jwt.encode(payload, secret, algorithm='HS256')
    return signature


def token_validator(token: str, secret: str = settings.SECRET_KEY) -> Tuple[bool, Union[str, dict]]:
    """验证token

    Args:
        token (str): token
        secret (str, optional): 秘钥. Defaults to settings.SECRET_KEY.

    Returns:
        Tuple[bool, Union[str, dict]]: token内容
    """
    try:
        payload = jwt.decode(token, secret, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return False, 'expired signature'
    except jwt.InvalidTokenError:
        return False, 'invalid token'
    else:
        return True, payload


def get_user_id_by_token(request):
    try:
        token_type, token = request.META.get("HTTP_AUTHORIZATION").split(None, 1)
    except (ValueError, AttributeError):
        raise ApiError(code='0401', message='请重新登录')

    if token == 'null' or token_type.lower() != 'bearer':
        raise ApiError(code='0401', message='请重新登录')

    result, token = token_validator(token)
    if not result:
        raise ApiError(code='0401', message='请重新登录')

    return token['sub']
