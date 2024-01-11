
from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

# from .utils.constants import PostStatus


@method_decorator(name='get', decorator=swagger_auto_schema(
    manual_parameters=[
        openapi.Parameter(
            'product_slug', openapi.IN_QUERY,
            description=("A unique string value identifying requested product"),
            type=openapi.TYPE_STRING,
            # enum=[ps.value for ps in ["SUCCESS", "FAIL"]],
            enum=[ps for ps in ["SUCCESS", "FAIL"]],
            required=True
        ),
    ]
))
class PingView(APIView):

    def get(self, *args, **kwargs):
        return Response({'ping': 'pong'}, status=status.HTTP_200_OK)