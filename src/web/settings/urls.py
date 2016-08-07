from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.global_settings_list, name='index'),
    url(r'^(?P<settings_item_id>[^/]+)/', views.process_edit_request, name='process_edit_request')
]
