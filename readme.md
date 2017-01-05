#### proxy是一套django开发的代理池项目
项目基于 dajngo1.8+ python3.x
在此环境下应该能无缝使用，其余版本没有测试但是应该没有问题，如有问题，欢迎想我提出
依赖
```
requests
BeautifulSoup4
```
你可以使用`pip`或者`easy_install`安装，也可以下载源代码然后使用`python setup.py isntall`安装。一切取决于你使用哪种方式更方便

### 使用方法
##### 1. 作为独立的app嵌入到你原有的项目中
你可以下载proxypool文件夹，放到你的django 项目中，在这种情况下，你只需要在做两步
    - 项目配置中的`INSTALLED_APPS`加入一行`'proxyPool.apps.ProxypoolConfig', `
    - 在 `urls.py`中加入的`urlpatterns`中加入路由配置`url(r'^proxyPool/', include('proxyPool.urls')),`

接着做好数据库的同步就好了
###### 2.作为完整的django项目:
你可以将proxyPool项目整个都copy回去,这里有些注意事项
    - db.sqlite3是我的demo数据库，里面有一些示例数据，后台账户为 `用户:qy  密码:1234abcd`
    - 你可以删除这个数据库文件重新生成

#### api说明
前提:假设你的host的`127.0.0.1::8000`
##### 1. xxx/proxyPool/get_client_ip
这是获取客户的ip的，返回格式是json字符串形式的ip地址，暂时未使用，但是我的想法是让他做代理可用性验证的，因为考虑到使用者有很大可能性本地部署所以此api未使用

##### 2. xxx/proxyPool/addxici
这是用来增加代理ip的,你应该定时访问他，时间间隔建议6小时一次
我这里写好了获取西祠国内匿名代理的demo,一般来说这就够用了，但是如果你需要可以按照我的实现方式增加别的获取方法

如果获取成功返回：json字符串形式的`添加一页代理数据成功`,
如果获取成功失败：`获取西祠代理失败："+错误原因`


##### 3. xxx/proxyPool/getproxy
get请求用来获取单个代理
他会随机的返回一个代理，但是你还是可以加上过滤条件abroad=x，x可选0：国内代理(默认)，1：国外代理

返回值类型:Json串
```
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
```

##### 4. xxx/proxyPool/get_dict_proxy
get请求用来获取多个代理
他会随机的返回指定个数的代理，
可选参数:
    - abroad=x，x可选0：国内代理(默认)，1：国外代理
    - count=x, x默认为1

返回值类型:Json串
```
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
    result  键result是一个包含所有代理信息的列表，列表中 的每个元素是一个字典，包含以下信息
        ip         代理ip
        port       代理ip的port
        protocol   代理的类型 HTTP还是HTTPS
        address    代理ip的所在地
        anonymous  是否是匿名的代理
        abroad     是否是国外的代理
        site       代理的来源站
```

##### 5. xxx/proxyPool/filter_proxy

验证代理ip可用性的接口,建议定时执行，建议时间间隔（30/60分钟一次）
返回结果："%s个代理失效了"+在此次验证中失效的代理个数
