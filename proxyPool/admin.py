from django.contrib import admin
from proxyPool.models import ProxyPool, Site


# 批量设置选中的为国外代理
def set_abroad(modeladmin, request, queryset):
    queryset.update(abroad=True)
set_abroad.short_description = "批量设置选中的为国外代理"


# 批量设置代理ip失效
def proxy_invalid(modeladmin, request, queryset):
    queryset.update(available=0)
proxy_invalid.short_description = "批量设置代理ip失效"


@admin.register(ProxyPool)
class ProxyPoolAdmin(admin.ModelAdmin):
    # 定义前端可显示的
    list_display = ('id', 'ip', 'port', 'protocol', 'anonymous', 'abroad', 'available', 'site', 'add_time')
    # 定义前端可编辑的
    list_editable = ('available', )
    actions = (set_abroad, proxy_invalid, )


@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    # 定义前端可显示的
    list_display = ('id', 'name', 'website',)
    list_display_links = ('id', 'name',)
    # 定义前端可编辑的
    # list_editable = ('name', 'website',)


# admin.site.register(ProxyPool)
# admin.site.register(ProxyPool, ProxyPoolAdmin)
