from django.contrib import admin
from proxyPool.models import ProxyPool


@admin.register(ProxyPool)
class ProxyPoolAdmin(admin.ModelAdmin):
    # 定义前端可显示的
    list_display = ('id', 'ip', 'port', 'protocol', 'address', 'anonymous', 'abroad', 'available')

# admin.site.register(ProxyPool)
# admin.site.register(ProxyPool, ProxyPoolAdmin)
