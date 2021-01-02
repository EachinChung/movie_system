import json

from django.views import View

from movie.models.user import User
from movie.request_models.user import UserBodyModel
from movie.utils.http_response import json_response, require_post


@require_post
def add_user(request):
    body = UserBodyModel(**json.loads(request.body))
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


class UserApi(View):
    """
    课程作业管理界面
    """

    @staticmethod
    def get(request):
        return json_response()

    @staticmethod
    def post(request):
        return json_response(code="FFFF")
