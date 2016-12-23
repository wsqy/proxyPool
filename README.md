1. 新建一个虚拟环境用于代理池项目
`python3 -m venv proxy`

2. 激活虚拟环境
`source proxy/bin/activate`

3. 查看下包
```
(proxy) ubuntu@VM-68-249-ubuntu:/soft$ pip freeze
pkg-resources==0.0.0
```

4. 安装依赖
```
pip install django
```

5. 新建一个django项目
```
django-admin startproject proxyTest
```
6. 进去项目，查看目录结构
```
├── manage.py
└── proxyTest
    ├── __init__.py
    ├── settings.py
    ├── urls.py
    └── wsgi.py
```

7. 启动下服务，看下效果   
看到 it worked就行

8. 新建app
```
python manage.py startapp proxyPool
```

9. 在项目的settings里注册app
```
# INSTALLED_APPS里增加下列任意一行，
# 下面一种是django1.8新加的方法   更灵活
# 我们使用下面一种
# 'proxyPool',
'proxyPool.apps.ProxypoolConfig'
```

10. 在项目的settings里做本地化
```
LANGUAGE_CODE = 'zh-Hans'
TIME_ZONE = 'Asia/Shanghai'
```

11. 数据库用自带的sqilte3就好了，需要的自己更改
```
# 这里维持不变，不需要改动或者添加下面的代码
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
```

### 代理池设计
1. 字段分析
```
IP
PORT
代理类型 (HTTP/HTTPS)
代理的归宿地  
是否是匿名的ip
是否是国外的ip
可用性(这里的可用性，是因为 免费的IP稳定性差  说不准啥时候就失效了，   我们在这里设置一个评分机制，初始为3分， 每次代理访问失败， 这里的可用性-1， 当可用性为0的时候  我们就认为其是无效的代理的  就不使用它了
)   
```
2. 根据字段分析 进行model设计
```
from django.db import models


# Create your models here.
class ProxyPool(models.Model):
    # verbose_name 这里是设置字段显示的名称
    ip = models.GenericIPAddressField(verbose_name="ip")
    port = models.SmallIntegerField(verbose_name="port")
    protocol = models.CharField(max_length=7, verbose_name="代理类型", default="HTTP")
    address = models.CharField(max_length=30, verbose_name="归宿地", default="")
    anonymous = models.BooleanField(verbose_name="是否匿名", default=1)
    abroad = models.BooleanField(verbose_name="是否是国外ip", default=0)
    available = models.SmallIntegerField(verbose_name="可用性", default=3)

    class Meta:
        # 设置的是后台显示表名  默认是类名
        verbose_name = "代理"
        # 是设置复数形式时显示的名称
        verbose_name_plural = "代理池"
        # 是设置某几个字段 联合起来在表中唯一
        unique_together = (("ip", "port"), )

    # 设置实例的显示值
    def __str__(self):
        return self.ip
```

3. 同步数据库
```
python manage.py makemigrations
python manage.py migrate

```


### 现在开始爬取部分

1. 安装依赖
```
pip install requests
pip install BeautifulSoup4
# 新建文件，import 他们
```

2. 爬取的目标是
```
http://www.xicidaili.com/
```
3. 为了防止反爬虫， 先把header保存下来
```
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
```
4. 使用request请求网页,下面的代码就可以获取网页内容了
```
# 我整理的常用requests用法http://note.youdao.com/noteshare?id=315ee85331c89f64bdd9810ef5f431d7
url = r'http://www.xicidaili.com/'
r = requests.get(url, headers=Headers, proxies=None)
print(r.text)
```

5. 结构分析

```
# 我整理的常用bs4用法 http://note.youdao.com/noteshare?id=752429deecdb4b12dd93583cfcac1493
```
