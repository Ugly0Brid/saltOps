from django.db.models import Q
from functools import reduce
from .models import DataCenter, Cabinet, Frame, Server, PmServer, VmServer, Group, Scope

RESOURCE_NAME = {
    "datacenter": DataCenter,
    "cabinet": Cabinet,
    "frame": Frame,
    "server": Server,
    "pmserver": PmServer,
    "vmserver": VmServer,
    "group": Group,
    "scope": Scope
}


def _pagination_filter_order(queryset, name, page, size, filter_dict, search_dict, exclude_dict, order):
    if filter_dict:
        for k, v in filter_dict.items():
            if isinstance(v, (list, tuple)):
                queryset = queryset.filter(**{'%s__in' % k: v})
            else:
                queryset = queryset.filter(**{k: v})
    if exclude_dict:
        for k, v in exclude_dict.items():
            if isinstance(v, (list, tuple)):
                queryset = queryset.exclude(**{'%s__in' % k: v})
            else:
                queryset = queryset.exclude(**{k: v})
    if search_dict:
        props = search_dict.get("properties")
        keyword = search_dict.get("keyword")
        q_list = [Q(**{'%s__icontains' % (prop): keyword}) for prop in props]
        queryset = queryset.filter(reduce(lambda x, y: x | y, q_list))
    queryset = queryset.order_by(order)
    queryset = queryset[(page - 1) * size:size]
    return queryset


def _select_params(name):
    item_list = list()
    if name == "datacenter":
        item_list = [{"id": item[0], "name": item[1]} for item in DataCenter.DATA_CENTER_TYPE]
    elif name == "cabinet":
        item_list = [{"id": item["id"], "name": item["name"]} for item in DataCenter.objects.values("id", "name")]
    elif name == "frame":
        item_list = [{"id": item["id"], "name": item["name"]} for item in Cabinet.objects.values("id", "name")]
    elif name in ["pmserver", "vmserver"]:
        frame_list = [{"frame_id": item["id"], "frame_name": item["name"]} for item in Frame.objects.values("id", "name")]
        scope_list = [{"scope_id": item["id"], "scope_name": item["name"]} for item in Scope.objects.values("id", "name")]
        minion_list = [{"id": item[0], "name": item[1]} for item in Server.MINION_STATUS]
        item_list = {"frame": frame_list, "scope": scope_list, "minion": minion_list}
    return item_list
