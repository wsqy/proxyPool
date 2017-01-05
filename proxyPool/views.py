import time
import json

import requests
from bs4 import BeautifulSoup

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from .models import ProxyPool
from .models import Site
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
OrigionalIP = requests.get("http://1212.ip138.com/ic.asp", headers=Headers).content


# Create your views here.
def addxici(request):
    """
    获取西祠 国内高匿代理 的首页100条数据
    """
    url = r'http://www.xicidaili.com/nn/'
    try:
        r = requests.get(url, headers=Headers, proxies=None)
        soup = BeautifulSoup(r.content, "html.parser")
        ListProxy = soup.find_all("tr")
    except Exception as e:
        mes = "获取西祠代理失败：%s" % e
        return mes
    else:
        try:
            siteinfo = Site.objects.get(name="西祠代理")
        except:
            siteinfo = Site.objects.create(name="西祠代理", website="http://www.xicidaili.com/")
        # 循环每条数据
        for i in ListProxy:
            info_list = {'anonymous': True, 'site': siteinfo}
            # 属性中没有 class属性代表就是标题，这种是跳过的
            if 'class' in i.attrs:
                infos = i.find_all("td")
                info_list["ip"] = infos[1].text.strip()
                info_list["port"] = infos[2].text.strip()
                info_list["address"] = infos[3].text.strip()
                info_list["protocol"] = infos[5].text.strip()
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
        # __gt 代表 大于 ; __gte 代表 大于或等于 ; lt 代表 小于 ; __lte 代表 小于或等于
        ipProxy = ProxyPool.objects.filter(available__gt=1, abroad=abroad).order_by('?')[0]
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
    ipProxylist = ProxyPool.objects.filter(available__gt=1, abroad=abroad).order_by('?')[0:count_proxy]
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
    for ipProxy in ipProxylist:
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


def testConnection(IP, PORT, PROTOCOL, REQ_TIMEOUT=2):
    指定 http和https请求都走我们获取的这个代理
    proxies = {
        "http": "%s://%s:%s" % (PROTOCOL.lower(), IP, PORT),
        "https": "%s://%s:%s" % (PROTOCOL.lower(), IP, PORT),
    }
    # 只有一致才任务代理是有效的  其余都是无效的
    try:
        MaskedIP = requests.get("http://1212.ip138.com/ic.asp", timeout=REQ_TIMEOUT, proxies=proxies, headers=Headers).content
        if OrigionalIP != MaskedIP:
            print("代理ok")
            return True
        else:
            print("代理失败")
            return False
    except Exception as e:
        print(e)
        print("---------")
        print("代理超时%s" % IP)
        print("---------")
        return False


def filter_proxy(request):
    """
    一次验证20个代理，失效的处理掉
    """
    # 随机取一个
    ipProxylist = ProxyPool.objects.order_by('?')[0:20]
    count = 0
    for ipProxy in ipProxylist:
        res = testConnection(ipProxy.ip, ipProxy.port, ipProxy.protocol)
        # 代理成功
        if res:
            if ipProxy.available == 3:
                # 可用性为3 不变
                pass
            else:
                # 可用性 小于3 则+1
                ipProxy.available += 1
                ipProxy.save()
        else:
            # 不成功-1,可用性为0则删除
            if ipProxy.available == 1:
                ipProxy.delete()
            else:
                ipProxy.available -= 1
                ipProxy.save()
            count += 1
    return HttpResponse("%s个代理失效了" % (count))


def get_client_ip(request):
    client_ip = request.META.get("REMOTE_ADDR", None)
    return HttpResponse(client_ip)
