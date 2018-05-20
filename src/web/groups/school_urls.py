from django.conf.urls import url

from groups.staff import views as staff_views

app_name = 'groups'


urlpatterns = [
    url(r'^$', staff_views.groups_list, name='list'),
    url(r'^data/$', staff_views.groups_list_data, name='list_data'),

    url(r'^(?P<group_name>[^/]+)/$', staff_views.group_info, name='group'),
    url(r'^(?P<group_name>[^/]+)/members/data/$', staff_views.members_data, name='members_data'),
]
