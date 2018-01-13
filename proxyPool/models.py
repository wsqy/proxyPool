from django.db import models
import django.utils.timezone as timezone


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


class ProxyPool(models.Model):
    # verbose_name 这里是设置字段显示的名称
    ip = models.GenericIPAddressField(verbose_name="ip")
    port = models.IntegerField(verbose_name="port")
    protocol = models.CharField(max_length=7, verbose_name="代理类型", default="HTTP")
    address = models.CharField(max_length=30, verbose_name="归宿地", default="")
    anonymous = models.BooleanField(verbose_name="是否匿名", default=True)
    abroad = models.BooleanField(verbose_name="是否是国外ip", default=False)
    available = models.SmallIntegerField(verbose_name="可用性", default=3)
    # 代理IP和站点是一对多的关系，设置下外键，default=1这里之前加的西祠代理 的id就是1
    site = models.ForeignKey(Site, verbose_name="站点", default=1)
    add_time = models.DateTimeField(default=timezone.now, verbose_name="创建时间")

    class Meta:
        # 设置的是后台显示表名  默认是类名
        verbose_name = "代理"
        # 是设置复数形式时显示的名称
        verbose_name_plural = "代理池"
        # 是设置某几个字段 联合起来在表中唯一
        unique_together = (("ip", "port"), )

    # 设置实例的显示值
    def __str__(self):
        return "%s:%s" % (self.ip, self.port)
