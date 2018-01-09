import os
import sys
import json
import random

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


result = []
proxy_base_url = r'http://proxy.viking666.com/proxyPool/proxy/'
def verify(proxy_info={}, _url='https://www.baidu.com'):
    _proxies = {
        "http": "http://%s:%s" % (proxy_info['ip'], proxy_info['port']),
        "https": "http://%s:%s" % (proxy_info['ip'], proxy_info['port']),
    }
    try:
        print("检测ip:--%s:%s" % (proxy_info['ip'], proxy_info['port']))
        with requests.session() as s:
            r = s.get(_url, proxies=_proxies, timeout=5, verify=False, allow_redirects=False)
    except Exception as e:
        print(e)
        pass
    else:
        # print("找到一个可用的ip")
        return proxy_info

def proxy(proxy_data):
    while len(proxy_data) > 0:
        print("还剩%s个待检测的ip" % len(proxy_data))
        _proxy = proxy_data.pop()
        res = verify(_proxy)
        if res:
            result.append(res)

def create_proxy(_proxy):
   try:
       with requests.session() as s:
           r = s.post(proxy_base_url, data=_proxy)
   except Exception as e:
       # print(e)
       pass

def delete_proxy(_proxy):
   try:
       with requests.session() as s:
           r = s.delete("%s/%s/" % (proxy_base_url, _proxy.get('id')))
   except Exception as e:
       print(e)
       pass

def main(proxy_data=None):
    gevent_task = []
    for each in range(20):
        gevent_task.append(gevent.spawn(proxy, proxy_data))
    gevent.joinall(gevent_task)
    print("总共%s个" % len(result))
    for _proxy in result:
        # print("第%s个" % _index)
        create_proxy(_proxy)


def filter_models():
    proxy_all = ProxyPool.objects.all()
    print(proxy_all.count())

def random_proxy():
    count = random.randint(10, 20)
    for i in range(count):
        print("第%s/%s尝试" % (i, count))
        try:
            with requests.session() as s:
                r = s.get(proxy_base_url)
                result = r.json().get('results')[0]
                if not verify(result):
                    delete_proxy(result)
        except Exception as e:
            print(e)
            pass

if __name__ == '__main__':
    random_proxy()
