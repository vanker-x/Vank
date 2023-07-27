# Created by vank
# DateTime: 2022/9/26-17:16
# Encoding: UTF-8
from vank.core.exceptions import NoneViewMethodException
from vank.core import request


class View:
    """
    通过类构建http请求方法对应类方法的视图
    子类至少实现一个http方法对应的类方法 否则会引发NoneViewMethodException异常
    例如:
     def get(self, *args, **kwargs):
         ...
         return Response

     def post(self, *args, **kwargs):
         ...
         return Response

    """

    @property
    def get_view_methods(self):
        http_methods = ["get", "post", "put", "patch", "delete", "head", "options", "trace"]
        allowed_methods = [method for method in http_methods if hasattr(self, method)]
        if not allowed_methods:
            raise NoneViewMethodException('The class view should define at least one '
                                          'method corresponding to the HTTP request method')
        return allowed_methods

    def get_response(self, *args, **kwargs):
        request_method: str = request.method
        return getattr(self, request_method.lower())(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        """
        视图的入口
        """
        return self.get_response(*args, **kwargs)

    @property
    def __name__(self):
        return self.__class__.__name__
