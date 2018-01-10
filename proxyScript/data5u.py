import sys
import json

import requests
from pyquery import PyQuery as pq
from verify_proxy import main as verify_main

Headers = {
    "Host": "www.data5u.com",
    "Cookie": "UM_distinctid=160a58675fe216-0f8ba03a9e12b8-61131b7e-13c680-160a58675ff17; Hm_lvt_3406180e5d656c4789c6c08b08bf68c2=1514605545; JSESSIONID=87EF7FFCCAB190DF6AAB1102AA26633C; CNZZDATA1260383977=220033334-1514603717-%7C1515560757; Hm_lpvt_3406180e5d656c4789c6c08b08bf68c2=1515561773",
    "User-Agent": r"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
    "Accept": r"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept_Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
    "Accept_Encoding": r"gzip, deflate",
    "Connection": r"keep-alive",
    "Cache-Control": r"max-age=0",
    "Upgrade-Insecure-Requests": "1",
    "Referer": r"http://www.data5u.com/free/index.shtml",
}

def data5u(_type='nn'):
    """
    获取西祠 国内高匿代理 的首页100条数据
    """
    # i = 0
    url = r'http://www.data5u.com/free/%s/index.shtml' % (_type)
    try:
        r = requests.get(url, headers=Headers, proxies=None)
        soup = pq(r.content)
        ListProxy = soup.find("ul.l2").items()
    except Exception as e:
        return
    else:
        info_list = []
        # 循环每条数据
        for proxy_item in ListProxy:
            info_dict = {
                "site": 3,
                "abroad": True,
                "anonymous": False,
            }
            infos = list(proxy_item.find("li").items())

            # for _index, info in enumerate(infos)
            info_dict["ip"] = infos[0].text().strip()
            info_dict["port"] = infos[1].text().strip()
            if infos[2].text().strip() in ('高匿', '匿名'):
                info_dict["anonymous"] = True
            info_dict["protocol"] = infos[3].text().strip()
            info_dict["address"] = "%s%s" % (infos[4].text().strip(), infos[5].text().strip())
            if infos[4].text().strip() == '中国':
                info_dict["abroad"] = False
            info_list.append(info_dict)
        return info_list



if __name__ == '__main__':
    # gngn 国内高匿   gnpt 国内普通   gwgn 国外高匿   gwpt 国外普通
    _type = sys.argv[1] if len(sys.argv)>1 else 'gngn'
    if _type in ('gngn', 'gnpt', 'gwgn', 'gwpt'):
        proxy_list = data5u(_type)
        verify_main(proxy_list)
