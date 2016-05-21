from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^table/(?P<table_name>[^/]+)/data/$', views.table_data, name='table_data'),
]
