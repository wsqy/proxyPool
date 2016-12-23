import requests
from bs4 import BeautifulSoup


Headers = {
    "Host": "fs.xicidaili.com",
    "Cookie": "CNZZDATA1256960793=1662416928-1459134890-%7C1461144106; _free_proxy_session=BAh7B0kiD3Nlc3Npb25faWQGOgZFVEkiJTUzYzVkYmViZWYzNDY5YjFlNWVhNjFkZDhlYWZkYTE2BjsAVEkiEF9jc3JmX3Rva2VuBjsARkkiMUI1aTgrenAzTXBiUVpqQ21CZjh4MlFQRE1RWjZJMzl3ZnNweEs2azhTc3c9BjsARg%3D%3D--2c0a55d5198a778ed50af34e2b356ab878c17d72",
    "User-Agent": r"Mozilla/5.0 (Windows NT 10.0; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0",
    "Accept": r"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept_Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
    "Accept_Encoding": r"gzip, deflate",
    "Connection": r"keep-alive",
    "Cache-Control": r"max-age=0",
}


def getinfo(url=None):
    if url is None:
        url = r'http://www.xicidaili.com/'
    try:
        r = requests.get(url, headers=Headers, proxies=None)
        soup = BeautifulSoup(r.text, "html.parser")
        ListProxy = soup.find_all("tr", limit=3)
        print(ListProxy)
    except Exception as e:
        mes = "获取西祠代理失败：%s" % e
        print(mes)


if __name__ == '__main__':
    # url = r'http://www.xicidaili.com/'
    # r = requests.get(url, headers=Headers, proxies=None)
    # print(r.text)
    p = getinfo()
