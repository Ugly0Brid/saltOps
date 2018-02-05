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
