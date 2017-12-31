# coding:utf-8
from . import views
from django.conf.urls import include, url

from rest_framework.routers import DefaultRouter

app_name = 'proxyPool'

router = DefaultRouter()
router.register(r'proxy', views.ProxyPoolViewset)

urlpatterns = [
    # rest framework 的路由
    url(r'^', include(router.urls)),
]
