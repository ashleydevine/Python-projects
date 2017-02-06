from django.conf.urls import url
from . import views

app_name = "wish_list"

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^wish_items/create$', views.create, name='create'),
    url(r'^wish_items/process$', views.process, name='process'),
    url(r'^wish_items/add/(?P<wish_id>\d+)$', views.add_item, name='add_item'),
    url(r'^wish_items/delete/(?P<wish_id>\d+)$', views.delete_item, name='delete_item'),
    url(r'^wish_items/remove/(?P<wish_id>\d+)$', views.remove_item, name='remove_item'),
    url(r'^wish_items/(?P<wish_id>\d+)$', views.wish_detail, name='wish_detail'),
    url(r'^logout$', views.logout),
]
