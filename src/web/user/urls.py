from django.conf.urls import patterns, url, include
from . import views

urlpatterns = patterns('',
                       url(r'^login/$', views.login, name='login'),
                       url(r'^logout/$', views.logout, name='logout'),
                       url(r'^register/', views.register, name='register'),
                       url(r'^complete/$', views.complete, name='complete'),
                       url(r'^confirm/(?P<token>[^/]+)', views.confirm, name='confirm'),
                       url('', include('social.apps.django_app.urls', namespace='social')),
                       )
