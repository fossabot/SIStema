from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns('',
                       url(r'^table/(?P<table_name>[^/]+)/data/$', views.table_data, name='table_data'),
                       )
