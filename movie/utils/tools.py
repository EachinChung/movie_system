import datetime
from typing import Union


def datetime2str(obj: Union[datetime.datetime, datetime.date]) -> str:
    """把日期对象转换成字符串

    Args:
        obj (Union[datetime.datetime, datetime.date]): 日期对象

    Returns:
        str: 时间字符串
    """
    if isinstance(obj, datetime.datetime):
        return obj.strftime('%Y-%m-%d %H:%M:%S')
    return obj.strftime("%Y-%m-%d")
