import datetime
from typing import Union


def datetime2str(obj: Union[datetime.datetime, datetime.date]):
    if isinstance(obj, datetime.datetime):
        return obj.strftime('%Y-%m-%d %H:%M:%S')
    return obj.strftime("%Y-%m-%d")
