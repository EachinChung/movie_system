import json

from django.views import View

from movie.constants.error_code import Error
from movie.decorators.auth import require_auth
from movie.models.user import User
from movie.request_models.user import UserPostModel, AuthPostModel, AuthPutModel
from movie.utils.http_response import json_response
from movie.utils.token import create_token, token_validator


class UserApi(View):

    @require_auth
    def get(self, request):
        """ 获取用户信息 """
        return json_response(data=request.user.to_dict())

    @staticmethod
    def post(request):
        """ 创建新用户 """
        body = UserPostModel(**json.loads(request.body))
        user = User.objects.get_by_email(body.email)
        if user:
            return json_response(code="FFFF", message="该邮箱已创建用户")

        user = User()
        user.nickname = body.nickname
        user.email = body.email
        user.sex = body.sex
        user.set_password(body.password)
        user.save()
        return json_response(message="用户注册成功")


class AuthApi(View):
    @staticmethod
    def post(request):
        """ 登录 """
        body = AuthPostModel(**json.loads(request.body))
        user = User.objects.get_by_email(body.email)
        code, message = Error.mail_or_password_error.unpack()
        if not user:
            return json_response(code=code, message=message)
        if not user.validate_password(body.password):
            return json_response(code=code, message=message)

        access_token = create_token(user.id)
        refresh_token = create_token(user.id, exp=43200)
        return json_response(data=dict(access_token=access_token, refresh_token=refresh_token))

    @staticmethod
    def put(request):
        """ 刷新登录状态 """
        body = AuthPutModel(**json.loads(request.body))
        result, token = token_validator(body.refresh_token)
        if not result:
            return json_response(code="FFFF", message=token)

        user_id = token['sub']
        access_token = create_token(user_id)
        refresh_token = create_token(user_id, exp=43200)
        return json_response(data=dict(access_token=access_token, refresh_token=refresh_token))
