import asyncio
import logging
from typing import Tuple, Union

from aiohttp import ClientSession

from movie.constants.error_code import Error
from movie.constants.muster import Method

logger = logging.getLogger('django')


class RequestsTool:
    @staticmethod
    async def __requests(method: str, is_json: bool = False, *args, **kwargs) -> Tuple[bool, Union[dict, str]]:
        """异步发送网络请求

        Args:
            method (str): 请求方法
            is_json (bool, optional): 返回格式是否为json. Defaults to False.

        Returns:
            Tuple[bool, Union[dict, str]]: 返回的数据
        """
        try:
            async with ClientSession() as session:
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

    async def get(self, is_json: bool = False, *args, **kwargs) -> Tuple[bool, Union[dict, str]]:
        return await self.__requests(Method.get, is_json, *args, **kwargs)

    async def post(self, is_json: bool = False, *args, **kwargs) -> Tuple[bool, Union[dict, str]]:
        return await self.__requests(Method.post, is_json, *args, **kwargs)

    async def put(self, is_json: bool = False, *args, **kwargs) -> Tuple[bool, Union[dict, str]]:
        return await self.__requests(Method.put, is_json, *args, **kwargs)

    async def patch(self, is_json: bool = False, *args, **kwargs) -> Tuple[bool, Union[dict, str]]:
        return await self.__requests(Method.patch, is_json, *args, **kwargs)

    async def delete(self, is_json: bool = False, *args, **kwargs) -> Tuple[bool, Union[dict, str]]:
        return await self.__requests(Method.delete, is_json, *args, **kwargs)


requests = RequestsTool()
