import json

import requests
from bs4 import BeautifulSoup

from django.shortcuts import render
from django.http import HttpResponse

from .models import ProxyPool
Headers = {
    "Host": "www.xicidaili.com",
    "Cookie": "CNZZDATA1256960793=1662416928-1459134890-%7C1461144106; _free_proxy_session=BAh7B0kiD3Nlc3Npb25faWQGOgZFVEkiJTUzYzVkYmViZWYzNDY5YjFlNWVhNjFkZDhlYWZkYTE2BjsAVEkiEF9jc3JmX3Rva2VuBjsARkkiMUI1aTgrenAzTXBiUVpqQ21CZjh4MlFQRE1RWjZJMzl3ZnNweEs2azhTc3c9BjsARg%3D%3D--2c0a55d5198a778ed50af34e2b356ab878c17d72",
    "User-Agent": r"Mozilla/5.0 (Windows NT 10.0; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0",
    "Accept": r"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept_Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
    "Accept_Encoding": r"gzip, deflate",
    "Connection": r"keep-alive",
    "Cache-Control": r"max-age=0",
}


# Create your views here.
def addxici(request):
    url = r'http://www.xicidaili.com/nn/'
    try:
        r = requests.get(url, headers=Headers, proxies=None)
        soup = BeautifulSoup(r.content, "html.parser")
        # ListProxy = soup.find_all("tr", limit=2)
        ListProxy = soup.find_all("tr")
    except Exception as e:
        mes = "获取西祠代理失败：%s" % e
        return mes
    else:
        # 循环每条数据
        for i in ListProxy:
            info_list = {'anonymous': True}
            # 属性中没有 class属性代表就是标题，这种是跳过的
            if 'class' in i.attrs:
                infos = i.find_all("td")
                # enumerate依次迭代
                for index, info in enumerate(infos):
                    if index == 1:
                        info_list["ip"] = info.text.strip()
                    elif index == 2:
                        info_list["port"] = info.text.strip()
                    elif index == 3:
                        info_list["address"] = info.text.strip()
                    elif index == 5:
                        info_list["protocol"] = info.text.strip()
                try:
                    ProxyPool.objects.create(**info_list)
                    print("添加成功")
                except Exception as e:
                    print("添加代理失败：%s" % e)
    return HttpResponse(json.dumps("添加一页代理数据成功"))
