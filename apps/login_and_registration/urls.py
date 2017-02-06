from django.conf.urls import url
from . import views

app_name = "login_and_registration"

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login$', views.login, name='login'),
    url(r'^register$', views.register, name='register'),
    url(r'^profile$', views.profile),
    url(r'^profile/(?P<id>\d+)/delete$', views.delete, name = 'my_delete'),
    url(r'^logout$', views.logout, name= 'logout'),
]
