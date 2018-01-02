import sys
import json

import requests
from pyquery import PyQuery as pq
from verify_proxy import main as verify_main

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

def addxici(_type='nn', _id=1):
    """
    获取西祠 国内高匿代理 的首页100条数据
    """
    # i = 0
    url = r'http://www.xicidaili.com/%s/%s' % (_type, _id)
    try:
        r = requests.get(url, headers=Headers, proxies=None)
        soup = pq(r.content)
        ListProxy = soup.find("tr").items()
    except Exception as e:
        return
    else:
        info_list = []
        # 循环每条数据
        for proxy_item in ListProxy:
            if proxy_item.attr('class') is not None:
                info_dict = {
                    "site": 1,
                    "abroad": False,
                    "anonymous": False,
                }
                infos = list(proxy_item.find("td").items())
                # for _index, info in enumerate(infos)
                info_dict["ip"] = infos[1].text().strip()
                info_dict["port"] = infos[2].text().strip()
                info_dict["address"] = infos[3].text().strip()
                info_dict["protocol"] = infos[5].text().strip()
                if infos[4].text().strip() == '高匿':
                    info_dict["anonymous"] = True
                info_list.append(info_dict)
        return info_list

    return


if __name__ == '__main__':
    _type = sys.argv[1] if len(sys.argv)>1 else 'nn'
    proxy_list = addxici(_type, 1)

    verify_main(proxy_list)
