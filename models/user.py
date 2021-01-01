from django.contrib.auth.hashers import check_password, make_password
from django.db import models

from constants.redis_cache_key import USER_CACHE_KEY
from models.base import BaseManager


class UserManager(BaseManager):
    def _get_cache_key(self, user_id: int) -> str:
        return USER_CACHE_KEY % user_id


class User(models.Model):
    nickname = models.CharField('昵称', max_length=30)
    sex = models.IntegerField('性别')
    email = models.CharField('邮箱', max_length=11)
    password_hash = models.CharField('密码', max_length=128)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)

    def set_password(self, password: str):
        """设置密码

        Args:
            password (str): 密码
        """
        self.password_hash = make_password(password)

    def validate_password(self, password: str) -> bool:
        """校验密码是否正确

        Args:
            password (str): 密码

        Returns:
            bool: 是否正确
        """
        return check_password(self.password_hash, password)
