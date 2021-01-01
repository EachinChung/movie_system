import asyncio
import logging
from typing import Tuple, Union

from aiohttp import ClientSession, ClientTimeout

from constants.error_code import Error
from constants.requests import REQUEST_TIMEOUT
from movie_system.settings import http_pool

logger = logging.getLogger('django')


async def get_request_pool():
    """获取http连接池

    Yields:
        ClientSession: 连接池
    """
    async with ClientSession(
            connector=http_pool,
            timeout=ClientTimeout(total=REQUEST_TIMEOUT),
            connector_owner=False,
    ) as session:
        yield session


class RequestsTool:
    @staticmethod
    async def requests(
            method: str,
            session: ClientSession,
            is_json: bool = False,
            *args, **kwargs
    ) -> Tuple[bool, Union[dict, str]]:
        """异步发送网络请求

        Args:
            method (str): 请求方法
            session (ClientSession): 连接池
            is_json (bool, optional): 返回格式是否为json. Defaults to False.

        Returns:
            Tuple[bool, Union[dict, str]]: 返回的数据
        """

        try:
            async with getattr(session, method)(*args, **kwargs) as response:
                if response.status == 200:
                    return True, await response.json() if is_json else await response.text()
                else:
                    code, message = Error.third_party_error.unpack()
                    return False, dict(code=code, message=message)

        except asyncio.TimeoutError:
            code, message = Error.timeout_error.unpack()
            return False, dict(code=code, message=message)

        except Exception as e:
            logger.exception(e)
            code, message = Error.request_error.unpack()
            return False, dict(code=code, message=message)


requests = RequestsTool()
