from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^questionnaire/(?P<questionnaire_name>[^/]+)/', views.questionnaire, name='questionnaire'),
    url(r'^settings/$', views.school_settings_list, name='school_settings_list'),
    url(r'^(?P<session_name>[^/]+)/settings/$', views.session_settings_list, name='session_settings_list'),
    url(r'^(?P<session_name>[^/]+)/mail/', views.mail, name='mail'),
    url(r'^mail/', views.common_mail, name='mail'),
    url(r'^settings/(?P<settings_item_id>[^/]+)/$', views.school_settings_item_edit, name='school_settings_item_edit'),
    url(r'^(?P<session_name>[^/]+)/settings/(?P<settings_item_id>[^/]+)/$', views.session_settings_item_edit, name='session_settings_item_edit'),
    # Modules
    url(r'^entrance/', include('modules.entrance.urls', namespace='entrance')),
    url(r'^topics/', include('modules.topics.urls', namespace='topics')),
    url(r'^finance/', include('modules.finance.urls', namespace='finance')),
]
