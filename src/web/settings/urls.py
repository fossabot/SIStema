from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'^$', views.global_settings_list, name='index'),
    url(r'^(?P<school_name>[^/]+)/$', views.school_settings_list, name='index'),
    url(r'^([^/]+)/(?P<session_name>[^/]+)/$', views.session_settings_list, name='index')
]
