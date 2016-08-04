from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'^$', views.global_settings_list, name='index'),
]
