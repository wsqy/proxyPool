# coding:utf-8
from . import views
from django.conf.urls import include, url

app_name = 'proxyPool'

urlpatterns = [
    url(r'^addxici', views.addxici, name='addxici'),
    url(r'^getproxy', views.getproxy, name='getproxy'),
]
