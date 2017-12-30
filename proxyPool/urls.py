# coding:utf-8
from . import views
from django.conf.urls import include, url

from rest_framework.routers import DefaultRouter

app_name = 'proxyPool'

router = DefaultRouter()
router.register(r'proxy', views.ProxyPoolViewset)

urlpatterns = [
    # url(r'^addxici', views.addxici, name='addxici'),
    # url(r'^getproxy', views.getproxy, name='getproxy'),
    # url(r'^get_dict_proxy', views.get_dict_proxy, name='get_dict_proxy'),
    # rest framework 的路由
    url(r'^', include(router.urls)),
]
