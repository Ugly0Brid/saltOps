from django.db import models

from django.utils import timezone


# Create your models here.
class BaseModel(models.Model):
    class Meta:
        abstract = True

    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="修改时间")
    remarks = models.TextField(verbose_name="备注", blank=True, null=True)


class DataCenter(BaseModel):
    class Meta:
        verbose_name = "机房"

    DATA_CENTER_TYPE = (
        (0, "线上机房"),
        (1, "容灾机房"),
    )
    name = models.CharField(max_length=255, verbose_name="名称")
    address = models.CharField(max_length=255, verbose_name="地址")
    data_center_type = models.IntegerField(verbose_name="类型", default=0, choices=DATA_CENTER_TYPE)
    link_name = models.CharField(max_length=255, verbose_name="联系人")
    band_width = models.CharField(max_length=255, verbose_name="带宽")
    contact_phone = models.CharField(max_length=255, verbose_name="联系人电话")

    def _to_dict(self):
        return {
            "id": self.id,
            "key": self.id,
            "name": self.name,
            "band_width": self.band_width,
            "type": DataCenter.DATA_CENTER_TYPE[self.data_center_type][1],
            "type_id": self.data_center_type,
            "address": self.address,
            "link_name": self.link_name,
            "contact_phone": self.contact_phone,
            "cabinet_count": self.cabinet_datacenter.count(),
            "create_time": self.create_time.strftime("%Y-%m-%d %H:%M:%S"),
            "update_time": self.update_time.strftime("%Y-%m-%d %H:%M:%S"),
            "remarks": self.remarks
        }

    def __str__(self):
        return self.name


class Cabinet(BaseModel):
    class Meta:
        verbose_name = "机柜"

    name = models.CharField(max_length=255, verbose_name="名称")
    data_center = models.ForeignKey(DataCenter, verbose_name="关联机房", related_name="cabinet_datacenter", blank=True, null=True)

    def _to_dict(self):
        return {
            "id": self.id,
            "key": self.id,
            "name": self.name,
            "frame_count": self.frame_cabinet.count(),
            "data_center": self.data_center.name if self.data_center else '',
            "data_center_id": self.data_center.id if self.data_center else '',
            "create_time": self.create_time.strftime("%Y-%m-%d %H:%M:%S"),
            "update_time": self.update_time.strftime("%Y-%m-%d %H:%M:%S"),
            "remarks": self.remarks
        }

    def __str__(self):
        return self.name


class Frame(BaseModel):
    class Meta:
        verbose_name = "机架"

    name = models.CharField(max_length=255, verbose_name="名称")
    cabinet = models.ForeignKey(Cabinet, verbose_name="关联机柜", related_name="frame_cabinet", blank=True, null=True)

    def _to_dict(self):
        return {
            "id": self.id,
            "key": self.id,
            "name": self.name,
            "cabinet": self.cabinet.name if self.cabinet else '',
            "cabinet_id": self.cabinet.id if self.cabinet else '',
            "server_count": self.server_frame.count(),
            "create_time": self.create_time.strftime("%Y-%m-%d %H:%M:%S"),
            "update_time": self.update_time.strftime("%Y-%m-%d %H:%M:%S"),
            "remarks": self.remarks
        }

    def __str__(self):
        return self.name


class Scope(BaseModel):
    class Meta:
        verbose_name = "领域"

    name = models.CharField(max_length=255, verbose_name="名称")
    label = models.CharField(max_length=255, verbose_name="标签")

    def _to_dict(self):
        return {
            "id": self.id,
            "key": self.id,
            "name": self.name,
            "label": self.label,
            "server_count": self.server_scope.count(),
            "create_time": self.create_time.strftime("%Y-%m-%d %H:%M:%S"),
            "update_time": self.update_time.strftime("%Y-%m-%d %H:%M:%S"),
            "remarks": self.remarks
        }

    def __str__(self):
        return self.name


class Server(BaseModel):
    class Meta:
        verbose_name = "服务器"

    MINION_STATUS = (
        (0, "未启动"),
        (1, "开启")
    )
    name = models.CharField(max_length=255, verbose_name="名称")
    minion_name = models.CharField(max_length=255, verbose_name="Minion名称")
    minion_status = models.IntegerField(verbose_name="Minion状态", default=1, choices=MINION_STATUS)
    os = models.CharField(max_length=255, verbose_name="OS")
    cpu = models.CharField(max_length=255, verbose_name="CPU")
    memory = models.CharField(max_length=255, verbose_name="内存")
    frame = models.ForeignKey(Frame, verbose_name="关联机架", related_name="server_frame", blank=True, null=True)
    scope = models.ManyToManyField(Scope, verbose_name="关联领域", related_name="server_scope", blank=True, null=True)
    class_name = models.CharField(verbose_name="类名", max_length=50)

    def save(self, *args, **kwargs):
        self.class_name = self.__class__.__name__
        super(Server, self).save(*args, **kwargs)

    def _to_dict(self):
        return {
            "id": self.id,
            "key": self.id,
            "name": self.name,
            "minion_name": self.minion_name,
            "minion_status": self.minion_status,
            "os": self.os,
            "cpu": self.cpu,
            "memory": self.memory,
            "frame": self.frame.name if self.frame else '',
            "scope": ",".join([item.name for item in self.scope.all()]),
            "create_time": self.create_time.strftime("%Y-%m-%d %H:%M:%S"),
            "update_time": self.update_time.strftime("%Y-%m-%d %H:%M:%S"),
            "remarks": self.remarks
        }

    def __str__(self):
        return self.name


class ServerIp(BaseModel):
    class Meta:
        verbose_name = "服务器IP"

    ip = models.CharField(max_length=255, verbose_name="服务器IP")
    mac = models.CharField(max_length=255, verbose_name="MAC地址")
    server = models.ForeignKey(Server, verbose_name="服务器", related_name="ip_server", blank=True, null=True)

    def __str__(self):
        return self.ip


class PmServer(Server):
    class Meta:
        verbose_name = "物理机"

    status = models.CharField(max_length=255, verbose_name="状态", blank=True, null=True)

    def _to_dict(self):
        return {
            "id": self.id,
            "key": self.id,
            "name": self.name,
            "ip": ",".join([item.ip for item in self.ip_server.all()]),
            "mac": ",".join([item.mac for item in self.ip_server.all()]),
            "minion_name": self.minion_name,
            "minion_status": Server.MINION_STATUS[self.minion_status][1],
            "minion_status_id": self.minion_status,
            "os": self.os,
            "cpu": self.cpu,
            "memory": self.memory,
            "frame": self.frame.name if self.frame else '',
            "frame_id": self.frame.id if self.frame else '',
            "scope": ",".join([item.name for item in self.scope.all()]),
            "scope_id": [item.id for item in self.scope.all()],
            "create_time": self.create_time.strftime("%Y-%m-%d %H:%M:%S"),
            "update_time": self.update_time.strftime("%Y-%m-%d %H:%M:%S"),
            "remarks": self.remarks
        }

    def __str__(self):
        return self.name


class VmServer(Server):
    class Meta:
        verbose_name = "虚拟机"

    pm_server = models.ForeignKey(PmServer, verbose_name="关联物理机", related_name="vm_pm", blank=True, null=True)

    def _to_dict(self):
        return {
            "id": self.id,
            "key": self.id,
            "name": self.name,
            "ip": ",".join([item.ip for item in self.ip_server.all()]),
            "mac": ",".join([item.mac for item in self.ip_server.all()]),
            "minion_name": self.minion_name,
            "minion_status": Server.MINION_STATUS[self.minion_status][1],
            "minion_status_id": self.minion_status,
            "os": self.os,
            "cpu": self.cpu,
            "memory": self.memory,
            "pm_server": self.pm_server.name if self.pm_server else '',
            "pm_server_id": self.pm_server.id if self.pm_server else '',
            "frame": self.frame.name if self.frame else '',
            "frame_id": self.frame.id if self.frame else '',
            "scope": ",".join([item.name for item in self.scope.all()]),
            "scope_id": [item.id for item in self.scope.all()],
            "create_time": self.create_time.strftime("%Y-%m-%d %H:%M:%S"),
            "update_time": self.update_time.strftime("%Y-%m-%d %H:%M:%S"),
            "remarks": self.remarks
        }

    def __str__(self):
        return self.name


class Group(BaseModel):
    class Meta:
        verbose_name = "组"

    name = models.CharField(max_length=255, verbose_name="名称")
    label = models.CharField(max_length=255, verbose_name="标签")

    def _to_dict(self):
        return {
            "id": self.id,
            "key": self.id,
            "name": self.name,
            "label": self.label,
            "create_time": self.create_time.strftime("%Y-%m-%d %H:%M:%S"),
            "update_time": self.update_time.strftime("%Y-%m-%d %H:%M:%S"),
            "remarks": self.remarks
        }

    def __str__(self):
        return self.name
