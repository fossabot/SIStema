"""sistema URL Configuration"""
from django.conf.urls import include, url
from modules.smartq import views

urlpatterns = [
  url('^heap/$', views.heap),
  url('^heap/(?P<seed>[^/]+)/$', views.heap),
]
