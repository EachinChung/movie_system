import asyncio

from django.utils.decorators import classonlymethod
from django.views import View


class AsyncApi(View):
    # noinspection PyUnresolvedReferences,PyProtectedMember
    @classonlymethod
    def as_view(cls, **kw):
        _view = super().as_view(**kw)
        _view._is_coroutine = asyncio.coroutines._is_coroutine
        return _view
