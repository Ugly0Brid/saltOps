from django.conf.urls import url
from resource_m import views

urlpatterns = [
    url(r'list/$', views.resource_list),
    url(r'create/', views.create_resource),
    url(r'update/', views.update_resource),
    url(r'delete/', views.delete_resource),
]
