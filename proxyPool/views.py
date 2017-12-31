from rest_framework import mixins, viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination

from .serializers import ProxyPoolSerializer
from .models import ProxyPool


class ProxyPagination(PageNumberPagination):
    page_size = 1
    page_size_query_param = 'size'
    page_query_param = "page"
    max_page_size = 20


class ProxyPoolViewset(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    create:
        创建代理
    list:
        获取代理列表数据
    retrieve:
        代理详情
    """
    filter_backends = (DjangoFilterBackend,)
    queryset = ProxyPool.objects.all().order_by('?')
    serializer_class = ProxyPoolSerializer
    pagination_class = ProxyPagination
    filter_fields = ('protocol', 'available', 'site')
    search_fields = ('address', )
