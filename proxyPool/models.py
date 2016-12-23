from django.db import models


# Create your models here.
class ProxyPool(models.Model):
    # verbose_name 这里是设置字段显示的名称
    ip = models.GenericIPAddressField(verbose_name="ip")
    port = models.SmallIntegerField(verbose_name="port")
    protocol = models.CharField(max_length=7, verbose_name="代理类型", default="HTTP")
    address = models.CharField(max_length=30, verbose_name="归宿地", default="")
    anonymous = models.BooleanField(verbose_name="是否匿名", default=True)
    abroad = models.BooleanField(verbose_name="是否是国外ip", default=False)
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
        return "%s:%s" % (self.ip, self.port)
