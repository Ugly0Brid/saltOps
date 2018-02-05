from django.contrib import admin
from .models import DataCenter, Cabinet, Frame, Scope, Server, PmServer, VmServer, Group

# Register your models here.



admin.site.register(DataCenter)
admin.site.register(Cabinet)
admin.site.register(Frame)
admin.site.register(Scope)
admin.site.register(Server)
admin.site.register(PmServer)
admin.site.register(VmServer)
admin.site.register(Group)


# 2.使用装饰器
# class PublisherAdmin(admin.ModelAdmin):
#     pass
