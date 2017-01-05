# coding:utf-8
from . import views
from django.conf.urls import include, url

app_name = 'proxyPool'

urlpatterns = [
    url(r'^addxici', views.addxici, name='addxici'),
    url(r'^getproxy', views.getproxy, name='getproxy'),
    url(r'^get_dict_proxy', views.get_dict_proxy, name='get_dict_proxy'),
    url(r'^filter_proxy', views.filter_proxy, name='filter_proxy'),
    url(r'^testmanage', views.testmanage, name='testmanage'),
]
