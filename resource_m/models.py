from django.db import models


# Create your models here.
class BaseModel(models.Model):
    class Meta:
        abstract = True

    create_time = models.DateTimeField(auto_now=True, verbose_name="创建时间")
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
            "name": self.name,
            "band_width": self.band_width,
            "type": self.data_center_type,
            "address": self.address,
            "link_name": self.link_name,
            "contact_phone": self.contact_phone,
            "create_time": self.create_time,
            "update_time": self.update_time,
            "remarks": self.remarks
        }

    def __str__(self):
        return self.name


class Cabinet(BaseModel):
    class Meta:
        verbose_name = "机柜"

    name = models.CharField(max_length=255, verbose_name="名称")
    data_center = models.ForeignKey(DataCenter, verbose_name="关联机房", related_name="cabinet_datacenter", blank=True,
                                    null=True)

    def _to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "data_center": self.data_center.name,
            "create_time": self.create_time,
            "update_time": self.update_time,
            "remarks": self.remarks
        }

    def __str__(self):
        return self.name


class Frame(BaseModel):
    class Meta:
        verbose_name = "机架"

    name = models.CharField(max_length=255, verbose_name="名称")
    cabinet = models.ForeignKey(Cabinet, verbose_name="关联机柜", auto_created="frame_cabinet", blank=True, null=True)

    def _to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "cabinet": self.cabinet.name,
            "create_time": self.create_time,
            "update_time": self.update_time,
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
            "name": self.name,
            "label": self.label,
            "create_time": self.create_time,
            "update_time": self.update_time,
            "remarks": self.remarks
        }

    def __str__(self):
        return self.name


class Server(BaseModel):
    class Meta:
        verbose_name = "服务器"

    MINION_STATUS = (
        (0, "关闭"),
        (1, "开启")
    )
    name = models.CharField(max_length=255, verbose_name="名称")
    minion_name = models.CharField(max_length=255, verbose_name="Minion名称")
    minion_status = models.IntegerField(verbose_name="Minion状态", default=0, choices=MINION_STATUS)
    os = models.CharField(max_length=255, verbose_name="OS")
    cpu = models.CharField(max_length=255, verbose_name="CPU")
    memory = models.CharField(max_length=255, verbose_name="内存")
    frame = models.ForeignKey(Frame, verbose_name="关联机架", related_name="server_frame", blank=True, null=True)
    scope = models.ManyToManyField(Scope, verbose_name="关联领域", related_name="server_scope", blank=True, null=True)

    def _to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "minion_name": self.minion_name,
            "minion_status": self.minion_status,
            "os": self.os,
            "cpu": self.cpu,
            "memory": self.memory,
            "frame": self.frame.name,
            "scope": ",".join([item.name for item in self.scope.all()]),
            "create_time": self.create_time,
            "update_time": self.update_time,
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
            "name": self.name,
            "minion_name": self.minion_name,
            "minion_status": self.minion_status,
            "os": self.os,
            "cpu": self.cpu,
            "memory": self.memory,
            "scope": ",".join([item.name for item in self.scope.all()]),
            "create_time": self.create_time,
            "update_time": self.update_time,
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
            "name": self.name,
            "minion_name": self.minion_name,
            "minion_status": self.minion_status,
            "os": self.os,
            "cpu": self.cpu,
            "memory": self.memory,
            "pm_server": self.pm_server.name,
            "scope": ",".join([item.name for item in self.scope.all()]),
            "create_time": self.create_time,
            "update_time": self.update_time,
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
            "name": self.name,
            "lable": self.label,
            "create_time": self.create_time,
            "update_time": self.update_time,
            "remarks": self.remarks
        }

    def __str__(self):
        return self.name
