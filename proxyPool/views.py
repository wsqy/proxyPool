import json

import requests
from bs4 import BeautifulSoup

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

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
    """
    获取西祠 国内高匿代理 的首页100条数据
    """
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


def getproxy(request):
    """
    获取代理的方法
    必有的返回参数
        code： 状态码
            000 未开始
            200 正常
            304 需求的代理暂时无法满足
            404 get请求abroad 参数类型错误
        mes :说明信息
    当请求成功，状态码为200时特有的参数
        ip         代理ip
        port       代理ip的port
        protocol   代理的类型 HTTP还是HTTPS
        address    代理ip的所在地
        anonymous  是否是匿名的代理
        abroad     是否是国外的代理
        site       代理的来源站
    """
    # 默认未开始
    res = {
        "code": 000,
        "mes": "NO Start"
    }

    # abroad看能不能转成整数，不能返回 4xx错误
    try:
        abroad = int(request.GET.get("abroad", 0))
    except Exception as e:
        res['code'] = 404
        res['mes'] = "abroad必须为整数,0代表获取一个国内代理,1代表获取一个国外代理"
        return JsonResponse(res)

    # 随机返回一个符合条件的代理，如果没有可用代理， 返回 3xx错误
    try:
        # order_by('?')表示乱序
        ipProxy = ProxyPool.objects.filter(available__gt=0, abroad=abroad).order_by('?')[0]
    except (IndexError, TypeError) as e:
        res['code'] = 304
        abroad = "国内" if abroad == 0 else "国外"
        res['mes'] = "暂无可用%s代理" % (abroad)
        return JsonResponse(res)
    else:
        res["code"] = 200
        res["mes"] = "获取代理成功"
        res["ip"] = ipProxy.ip
        res["port"] = ipProxy.port
        res["protocol"] = ipProxy.protocol
        res["address"] = ipProxy.address
        res["anonymous"] = ipProxy.anonymous
        res["abroad"] = ipProxy.abroad
        res["site"] = ipProxy.site.name
    return JsonResponse(res)


def get_dict_proxy(request):
    """
    获取代理的方法, 可以指定数量
    必有的返回参数
        code： 状态码
            000 未开始
            200 正常
            201 爬取成功 数量不足要求
            304 需求的代理暂时无法满足
            404 get请求abroad 参数类型错误
        mes: 说明信息
    当请求成功，状态码为2xx时特有的参数
        count   返回代理的个数
        result  键result是一个包含所有代理信息的列表
            ip         代理ip
            port       代理ip的port
            protocol   代理的类型 HTTP还是HTTPS
            address    代理ip的所在地
            anonymous  是否是匿名的代理
            abroad     是否是国外的代理
            site       代理的来源站
    """
    # 默认未开始
    res = {
        "code": 000,
        "mes": "NO Start"
    }
    # abroad看能不能转成整数，不能返回 4xx错误
    try:
        abroad = int(request.GET.get("abroad", 0))
    except Exception as e:
        res['code'] = 404
        res['mes'] = "参数错误:abroad必须为整数,0代表获取一个国内代理,1代表获取一个国外代理"
        return JsonResponse(res)

    # count看能不能转成整数，不能返回 4xx错误
    try:
        count_proxy = int(request.GET.get("count", 1))
    except Exception as e:
        res['code'] = 404
        res['mes'] = "参数错误:返回的代理个数必须是整数"
        return JsonResponse(res)

    # order_by('?')表示乱序
    ipProxylist = ProxyPool.objects.filter(available__gt=0, abroad=abroad).order_by('?')[0:count_proxy]
    ProxylistLen = len(ipProxylist)
    if ProxylistLen == 0:
        res["code"] = 304
        res['mes'] = "暂无可用代理"
        return JsonResponse(res)
    # 键result是一个包含所有代理信息的列表
    res['result'] = []
    res['count'] = ProxylistLen
    if ProxylistLen < count_proxy:
        res['code'] = 201
        res['mes'] = "代理数量不足"
    else:
        res['code'] = 200
        res['mes'] = "获取代理成功"
    # 循环结果 加入结果集
    for ipProxy ipProxylist:
        ress = {}
        ress["ip"] = ipProxy.ip
        ress["port"] = ipProxy.port
        ress["protocol"] = ipProxy.protocol
        ress["address"] = ipProxy.address
        ress["anonymous"] = ipProxy.anonymous
        ress["abroad"] = ipProxy.abroad
        ress["site"] = ipProxy.site.name
        res['result'].append(ress)
    return JsonResponse(res)


def testmanage(request):
    return HttpResponse("test")
