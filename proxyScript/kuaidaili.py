import sys
import json

import requests
from pyquery import PyQuery as pq
from verify_proxy import main as verify_main

Headers = {
    "Host": "www.kuaidaili.com",
    "Cookie": "channelid=0; Hm_lvt_7ed65b1cc4b810e9fd37959c9bb51b31=1515565647; _ga=GA1.2.2085532678.1515565648; _gid=GA1.2.386397238.1515565648; _gat=1; sid=1515572244124636; Hm_lpvt_7ed65b1cc4b810e9fd37959c9bb51b31=1515572518",
    "User-Agent": r"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
    "Accept": r"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept_Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
    "Accept_Encoding": r"gzip, deflate",
    "Connection": r"keep-alive",
    "Cache-Control": r"max-age=0",
    "Upgrade-Insecure-Requests": "1",
    "Referer": r"https://www.kuaidaili.com/free/intr/",
}

def kuaidaili(_type='inha'):
    """
    """
    url = r'https://www.kuaidaili.com/free/%s' % (_type)
    try:
        r = requests.get(url, headers=Headers, proxies=None)
        soup = pq(r.content)
        ListProxy = soup.find("#list tbody tr").items()
    except Exception as e:
        print("获取页面错误--%s" % e)
        return
    else:
        info_list = []
        # 循环每条数据
        for proxy_item in ListProxy:
            info_dict = {
                "site": 5,
                "abroad": False,
                "anonymous": True,
            }
            infos = list(proxy_item.find("td").items())

            # for _index, info in enumerate(infos)
            info_dict["ip"] = infos[0].text().strip()
            info_dict["port"] = infos[1].text().strip()
            if infos[2].text().strip() == '透明':
                info_dict["anonymous"] = False
            info_dict["protocol"] = infos[3].text().strip()
            info_dict["address"] = infos[4].text().strip()
            info_list.append(info_dict)
        return info_list



if __name__ == '__main__':
    _type = sys.argv[1] if len(sys.argv)>1 else 'inha'
    if _type in ('inha', 'intr'):
        proxy_list = kuaidaili(_type)
        if proxy_list:
            verify_main(proxy_list)
