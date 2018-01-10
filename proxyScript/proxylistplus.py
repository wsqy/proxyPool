import sys
import json

import requests
from pyquery import PyQuery as pq
from verify_proxy import main as verify_main

Headers = {
    "Host": "list.proxylistplus.com",
    "Cookie": "__cfduid=db646f1c3492e1d3604d947de08fe8a6d1515564484; _ga=GA1.2.409120336.1515564484; _gid=GA1.2.1086588610.1515564484; _first_pageview=1; _jsuid=2937446581; no_trackyy_100814458=1; _gat=1; __atuvc=3%7C2; __atuvs=5a55adc45fa1361f002; _eventqueue=%7B%22heatmap%22%3A%5B%7B%22type%22%3A%22heatmap%22%2C%22href%22%3A%22%2FSocks-List-1%22%2C%22x%22%3A740%2C%22y%22%3A47%2C%22w%22%3A1440%7D%5D%2C%22events%22%3A%5B%5D%7D",
    "User-Agent": r"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
    "Accept": r"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept_Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
    "Accept_Encoding": r"gzip, deflate",
    "Connection": r"keep-alive",
    "Cache-Control": r"max-age=0",
    "Upgrade-Insecure-Requests": "1",
    "Referer": r"http://list.proxylistplus.com/update-2",
}

def data5u(_i=1):
    """
    获取西祠 国内高匿代理 的首页100条数据
    """
    # i = 0
    url = r'http://list.proxylistplus.com/Fresh-HTTP-Proxy-List-%i' % (_i)
    try:
        r = requests.get(url, headers=Headers, proxies=None)
        soup = pq(r.content)
        ListProxy = soup.find("tr.cells").items()
    except Exception as e:
        return
    else:
        info_list = []
        # 循环每条数据
        for proxy_item in ListProxy:
            info_dict = {
                "site": 4,
                "abroad": True,
                "anonymous": True,
                "protocol": "HTTPS",
            }
            infos = list(proxy_item.find("td").items())

            info_dict["ip"] = infos[1].text().strip()
            info_dict["port"] = infos[2].text().strip()
            if infos[3].text().strip().lower() == 'elite':
                info_dict["anonymous"] = False
            info_dict["address"] = infos[4].text().strip()
            if infos[6].text().strip().lower() == 'no':
                info_dict["protocol"] = 'HTTP'
            if infos[4].text().strip().lower() == 'china':
                info_dict["abroad"] = False
            info_list.append(info_dict)
        return info_list


if __name__ == '__main__':
    proxy_list = data5u(1)
    if proxy_list:
        verify_main(proxy_list)
