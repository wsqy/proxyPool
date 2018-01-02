import os
import sys
import json

import gevent
import requests
from gevent import monkey
monkey.patch_all()


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.insert(0, BASE_DIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "proxyTest.settings")
import django
django.setup()

from proxyPool.models import ProxyPool

#
# import sys
# sys.setrecursionlimit(1000000)


result = []
proxy_create_url = r'http://proxy.viking666.com/proxyPool/proxy/'
def verify(proxy_info={}, url='https://www.baidu.com'):
    _proxies = {
        "http": "%s://%s:%s" % (proxy_info['protocol'].lower(), proxy_info['ip'], proxy_info['port']),
        "https": "%s://%s:%s" % (proxy_info['protocol'].lower(), proxy_info['ip'], proxy_info['port']),
    }
    try:
        print("检测ip:--%s:%s" % (proxy_info['ip'], proxy_info['port']))
        r = requests.get(url, proxies=_proxies, timeout=5, verify=False)
    except Exception as e:
        pass
    else:
        print("找到一个可用的ip")
        result.append(proxy_info)

def proxy(proxy_data):
    while len(proxy_data) > 0:
        print("还剩%s个待检测的ip" % len(proxy_data))
        _proxy = proxy_data.pop()
        verify(_proxy)

def create_proxy():
    for _index, _proxy in enumerate(result):
        print("第%s个" % _index)
        r = requests.post(proxy_create_url, data=_proxy)

def main(proxy_data=None):
    gevent_task = []
    for each in range(50):
        gevent_task.append(gevent.spawn(proxy, proxy_data))
    gevent.joinall(gevent_task)
    print("总共%s个" % len(result))
    create_proxy()

def filter_models():
    proxy_all = ProxyPool.objects.all()
    print(proxy_all.count())

if __name__ == '__main__':
    filter_models()