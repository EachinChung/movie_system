import abc

from django.core.cache import cache
from django.db import models


class BaseManager(models.Manager):
    """ orm 管理基类 """
    @abc.abstractmethod
    def _get_cache_key(self, model_id: int) -> str:
        """获取缓存的key

        Args:
            model_id (int): id

        Raises:
            NotImplementedError: 没有重写改方法

        Returns:
            str: key
        """
        raise NotImplementedError()

    def get_by_id(self, model_id: int) -> models.Model:
        """通过id查询数据，有60秒缓存

        Args:
            model_id (int): id

        Returns:
            models.Model: 数据的映射关系
        """
        key = self._get_cache_key(model_id)
        model = cache.get(key)
        if not model:
            model = self.filter(id=model_id).first()
            cache.set(key, model, timeout=60)
        return model
