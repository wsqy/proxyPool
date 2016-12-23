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

```
看到 it worked就行
```

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
