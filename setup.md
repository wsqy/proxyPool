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

4. 创建用户

```
python manage.py createsuperuser  用户:qy  密码:1234abcd
python manage.py changepassword
```

5. 在admin.py里注册自己的应用
```
from proxyPool.models import ProxyPool
@admin.register(ProxyPool)
class ProxyPoolAdmin(admin.ModelAdmin):
    # 定义前端可显示的
    list_display = ('id', 'ip', 'port', 'protocol', 'address', 'anonymous', 'abroad', 'available')
# admin.site.register(ProxyPool)
# admin.site.register(ProxyPool, ProxyPoolAdmin)
```

6. 增加咱自己的批量动作
```
# 批量设置代理ip失效
def proxy_invalid(modeladmin, request, queryset):
    queryset.update(available=0)
proxy_invalid.short_description = "批量设置代理ip失效"

actions = (set_abroad, proxy_invalid, )
```



### 现在开始爬取部分

1. 安装依赖
```
pip install requests
pip install BeautifulSoup4
# 新建文件，import 他们
import requests
from bs4 import BeautifulSoup
```

2. 爬取的目标是
```
http://www.xicidaili.com/nn/
```

3. 为了防止反爬虫， 先把header保存下来
```
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
soup = BeautifulSoup(r.content, "html.parser")
ListProxy = soup.find_all("tr")
# 我整理的常用bs4用法 http://note.youdao.com/noteshare?id=752429deecdb4b12dd93583cfcac1493
```


6. 在项目里包含路由
```
#
from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^proxyPool/', include('proxyPool.urls')),
]
```

7. 在app里 增加路由
```
from . import views
from django.conf.urls import include, url

app_name = 'proxyPool'

urlpatterns = [
    url(r'^addxici', views.addxici, name='addxici'),
]
```

8. 在views里简单写个 addxici函数 测试下
```
from django.http import HttpResponse


# Create your views here.
def addxici(request):
    return HttpResponse("it's ok")
```


9. 把爬取的代码贴到adxici里
```
import json

import requests
from bs4 import BeautifulSoup

from django.shortcuts import render
from django.http import HttpResponse

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
        proxy_all = []
        for i in ListProxy:
            info_list = {'anonymous': True}
            # 属性中没有 class属性代表就是标题，这种是跳过的
            if 'class' in i.attrs:
                infos = i.find_all("td")
                info_list["ip"] = infos[1].text.strip()
                info_list["port"] = infos[2].text.strip()
                info_list["address"] = infos[3].text.strip()
                info_list["protocol"] = infos[5].text.strip()
                # print(info_list)
            proxy_all.append(info_list)
    return HttpResponse(json.dumps(proxy_all))
```

10. 加载数据库模型
```
from .models import ProxyPool
```

11. 存数据库，修改addxic代码
```
修改 print(info_list) 改为：
try:
    ProxyPool.objects.create(**info_list)
    print("添加成功")
except Exception as e:
    print("添加代理失败：%s" % e)

删除 proxy_all.append(info_list)

修改 return HttpResponse(json.dumps(proxy_all))  改为  return HttpResponse(json.dumps("添加一页代理数据成功"))
```


#### 代理池项目进阶
我们之前只爬取了 西祠的代理  一般情况下就够用了  但是如果我们想爬取多个网站的时候  最好还是要标明一下 代理的来源的  
所以  首先加个站点记录：站点表需要 有 站点名  网址 邮箱
```
class Site(models.Model):
    """
    站点表需要 有 站点名  网址 邮箱(基本不需要，这里添加在这里是为了给大家展示怎么设置 字段可以为空）
    """
    # 必须要有 max_length参数 verbose_name定义展示的时候字段的显示出来的名字
    name = models.CharField(max_length=30, verbose_name="网站名")
    # EmailField是django在CharField上扩展定义的  会对字符串做是否是邮箱的检查；blank=True 代表可以为空白
    email = models.EmailField(blank=True, verbose_name="邮箱")
    # URLField是django在CharField上扩展定义的  会对字符串做是否是网址的检查；如果只需要定义一个 verbose_name，可以省略
    website = models.URLField("网址")

    class Meta:
        verbose_name = "站点"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
```

好同步一下看下:

```
python manage.py makemigrations
python manage.py migrate
```
这时候注册模型到后台管理界面
```
from proxyPool.models import Site
admin.site.register(Site)
```
增加一条 西祠网站的记录
```
西祠代理  http://www.xicidaili.com  邮箱留空
```

扩展下站点的admin注册类：
```
@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    # 定义前端可显示的
    list_display = ('id', 'name', 'email', 'website',)
    # 定义前端可编辑的
    list_editable = ('name', 'website',)
```


我们的代理ip，就需要设置一下来源了
代理IP和站点是一对多的关系，设置下外键
```
class ProxyPool(models.Model):
    .....
    site = models.ForeignKey(Site, verbose_name="站点", default=1)
```
同步一下看下:

```
python manage.py makemigrations
python manage.py migrate
```

代理的注册类修改下:
```
    ...
    list_display = ('id', 'ip', 'port', 'protocol', 'address', 'anonymous', 'abroad', 'available', 'site', )
    ....
```


准备工作 做好了  现在  访问下 url(r'^addxici', views.addxici, name='addxici')  这是增加代理的接口

蹬蹬瞪    又增加了差不多100个代理


再看下调用api获取一个代理的方法
url(r'^getproxy', views.getproxy, name='getproxy'),

返回值
```
{"address": "\u6d59\u6c5f\u676d\u5dde", "code": 200, "port": 80, "anonymous": true, "abroad": false, "protocol": "HTTP", "ip": "183.129.151.130"}
```


你会发现 不管你调用多少遍   返回的代理都是同一个   为什么呢？？？  看views中
```
def getproxy(request):
    ipProxy = ProxyPool.objects.filter(available__gt=0)[0]
    .....
```
都是返回第一个  这里我们要修改一下   返回的应该是 随机的一个
我查阅文档是好像是没有发现有提供随机返回一个的方法的
我这里准备使用一个比较高级的方法   自定义objects管理器的方法
我们所有的方法比如 filter  count 等等都是objects给我们提供的方法   那么很自然的 如果 他没有提供给我们一个方法  我们只需要继承，扩展他就好了，这里我们 定义一个管理器ProxyManager继承原有的管理器

在models里定义一个管理器
```
class ProxyManager(models.Manager):
    """
    自定义代理池的管理器，主要是为了提供一个随机获取的方法
    """
    def hello(self):
        return "11qq"
```

还要记得在模型里加上这一句话:
```
objects = ProxyManager()
```
现在实现一个views
```
def testmanage(request):
    ipProxy = ProxyPool.objects.hello()
    return HttpResponse(json.dumps(ipProxy))
```
这里的结果应该就是返回 '11qq'了

设置一个路由 ：
url(r'^testmanage', views.testmanage, name='testmanage'),

测试 没有问题了


这时候Ryan给我提供一个方法:order_by("?")这里就是随机取了
试验下:
修改 views里的代码 :
```
ipProxy = ProxyPool.objects.filter(available__gt=0).order_by('?')[0]
```

发现确实能够随机取，为了看下sql在settings里增加一个日志的配置，使用我配置的日志器 需要在项目文件夹中新建文件夹log【app同级目录】
```
日志配置的详细代码查看github
https://github.com/wsqy/proxyPool/blob/master/proxyTest/settings.py#L124
```

发现 order_by("?") 其实就是 ORDER BY RANDOM()


开始完善api ，现在能提供一个代理了  那如果客户需要指定我就用国外代理怎么办呢，  我们可以 用get请求  直接加个参数就行了

```
"""
获取代理的方法
必有的返回参数
    code： 状态码
        000 未开始
        200 正常
        304 需求的代理暂时无法满足
        404 get请求abroad 参数类型错误
当请求成功，状态码为200时特有的参数
    ip         代理ip
    port       代理ip的port
    protocol   代理的类型 HTTP还是HTTPS
    address    代理ip的所在地
    anonymous  是否是匿名的代理
    abroad     是否是国外的代理
    site       代理的来源站
"""
getproxy详细代码 参考views.py
````

获取单个代理的方法我们已经知道了，这在一般情况中，我们应该已经就够用了

现在来看另外一个需求:怎么一次获取一批代理呢?
这个方法可以通过多次调用我们的getproxy方法，但是我们这里不这样做，我们写一个批量获取代理的views:get_dict_proxy
我们其实也可以改造 getproxy视图，加一个参数就可以实现了，但是由于获取批量需求比较少，所以在这里单独写一个视图，并做好映射:url(r'^get_dict_proxy', views.get_dict_proxy, name='get_dict_proxy'),

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
```
get_dict_proxy查看views的相应部分
```

免费的代理肯定是有很多问题的，说不定什么时候就失效了， 我们防止失效用的是加了一个字段 available ，分值0-3，在api调用的时候 只过滤分值大于1的代理

但是到目前为止我们都还没有 做可用性的调整，导致我们随机取出一个给调用api的用户确并不能保证可用性的尴尬
为了防止此问题我们可用写一个视图随机取出ip并验证是否可用的视图，如果可用，且分值小于3则加1，如果是3则不变，如果不可用则分值减1，分值为0 则删除此代理

我们新建一个视图
```
def filter_proxy(request):
    return HttpResponse(json.dumps("过滤成功一次"))
```
并且建立好映射:
```
url(r'^filter_proxy', views.filter_proxy, name='filter_proxy'),
```

测试代理是否失效的方案:轮流访问一个可用查看自己ip的网站，如果两次的ip不一致，则代理成功，否则，代理失败，在一定量时间没有请求响应也算请求失败
暂时使用的是[ip138 http://1212.ip138.com/ic.asp](http://1212.ip138.com/ic.asp)的ip查看页
