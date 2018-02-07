from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User, Group
from django.http import JsonResponse
from rest_framework import viewsets
from django.db import transaction
import json

from .models import DataCenter, Cabinet, Frame, Scope, PmServer, Group
from .common import RESOURCE_NAME, _pagination_filter_order
from .serializers import UserSerializer, GroupSerializer
from .common import _select_params


# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


def resource_list(request):
    page = request.GET.get("page", "1")
    size = request.GET.get("size", "10")
    resource_name = request.GET.get("name", None)
    order = request.GET.get("order", "-create_time")
    filter_dict = request.GET.get("filter_dict", "{}")
    search_dict = request.GET.get("search_dict", "{}")
    exclude_dict = request.GET.get("exclude_dict", "{}")
    if not resource_name or resource_name not in RESOURCE_NAME:
        return JsonResponse({"status": -1, "error": "参数错误."})
    try:
        page = int(page)
        size = int(size)
        filter_dict = json.loads(filter_dict)
        search_dict = json.loads(search_dict)
        exclude_dict = json.loads(exclude_dict)
        queryset = RESOURCE_NAME[resource_name].objects.all()
        count = queryset.count()
        item_list = list()
        queryset = _pagination_filter_order(queryset, resource_name, page, size, filter_dict, search_dict, exclude_dict, order)
        for item in queryset:
            item_list.append(item._to_dict())
        return JsonResponse({"status": 0, "item_list": item_list, "count": count, "current": page, "select_list": _select_params(resource_name)})
    except Exception as e:
        print(str(e))
        return JsonResponse({"status": -1, "error": "获取数据失败."})


@csrf_exempt
def create_resource(request):
    params = request.body.decode()
    params = json.loads(params)
    resource_name = params.get("resource_name", None)
    if resource_name not in RESOURCE_NAME:
        return JsonResponse({"status": -1, "error": "参数错误."})
    try:
        params.pop("resource_name")
        if resource_name == "cabinet":
            data_center_id = params.get("data_center")
            if data_center_id:
                params.pop("data_center")
                params["data_center"] = DataCenter.objects.filter(pk=data_center_id).first()
        elif resource_name == "frame":
            cabinet_id = params.get("cabinet")
            if cabinet_id:
                params.pop("cabinet")
                params["cabinet"] = Cabinet.objects.filter(pk=cabinet_id).first()
        elif resource_name in ["pmserver", "vmserver"]:
            frame_id = params.get("frame")
            scope_id = params.get("scope")
            if frame_id:
                params.pop("frame")
                params["frame"] = Frame.objects.filter(pk=frame_id).first()
            if scope_id:
                params.pop("scope")
            if params.get("mac", None):
                params.pop("mac")
            if resource_name == "vmserver":
                pm_server_id = params.get("pm_server_id")
                if pm_server_id:
                    params.pop("pm_server_id")
                    params["pm_server"] = PmServer.objects.filter(pk=pm_server_id).first()
            params.pop("ip")

            obj = RESOURCE_NAME[resource_name].objects.create(**params)
            try:
                if scope_id:
                    for item in Scope.objects.filter(pk__in=scope_id).all():
                        obj.scope.add(item)
                return JsonResponse({"status": 0})
            except Exception as e:
                obj.delete()
                return JsonResponse({"status": -1, "error": "创建资源失败."})
        RESOURCE_NAME[resource_name].objects.create(**params)
        return JsonResponse({"status": 0})
    except Exception as e:
        print(str(e))
        return JsonResponse({"status": -1, "error": "创建资源失败."})


@csrf_exempt
def update_resource(request):
    params = request.body.decode()
    params = json.loads(params)
    resource_name = params.get("resource_name", None)
    id = params.get("id", None)
    if resource_name not in RESOURCE_NAME or not id:
        return JsonResponse({"status": -1, "error": "参数错误."})
    params.pop("resource_name")
    if resource_name in ["pmserver", "vmserver"]:
        scope_id = params.get("scope", None)
        params.pop("scope")
        if params.get("mac", None):
            params.pop("mac")
        params.pop("ip")
        if scope_id:
            try:
                with transaction.atomic():
                    obj = RESOURCE_NAME[resource_name].objects.filter(pk=id)
                    obj.update(**params)
                    for item in obj.first().scope.all():
                        obj.first().scope.remove(item)
                    for item in Scope.objects.filter(pk__in=scope_id).all():
                        obj.first().scope.add(item)
                return JsonResponse({"status": 0})
            except Exception as e:
                print(str(e))
                return JsonResponse({"status": -1, "error": "更新数据失败,传入参数错误."})
    try:
        RESOURCE_NAME[resource_name].objects.filter(pk=id).update(**params)
        return JsonResponse({"status": 0})
    except Exception as e:
        print(str(e))
        return JsonResponse({"status": -1, "error": "更新数据失败."})


def delete_resource(request):
    try:
        params = request.GET
        ids = params.get("id", None)
        resource_name = params.get("name", None)
        if resource_name not in RESOURCE_NAME or not ids:
            return JsonResponse({"status": -1, "error": "参数错误."})
        ids = json.loads(ids)
        RESOURCE_NAME[resource_name].objects.filter(pk__in=ids).delete()
        return JsonResponse({"status": 0})
    except Exception as e:
        print(str(e))
        return JsonResponse({"status": -1, "error": "删除资源失败."})
