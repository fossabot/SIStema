from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.inbox, name='inbox'),
    url(r'^compose/', views.compose, name='compose'),
    url(r'^contacts/', views.contacts, name='contacts'),
    url(r'^sent/', views.sent, name='sent'),
    url(r'^webhook/', views.incoming_webhook),
    url(r'^attachment/(?P<attachment_id>[^/]+)/', views.download_attachment, name='download_attachment'),
    url(r'^(?P<message_id>[^/]+)/$', views.message, name='message'),
    url(r'^(?P<message_id>[^/]+)/delete/', views.delete_email, name='delete'),
    url(r'^(?P<message_id>[^/]+)/reply/', views.reply, name='reply'),
]
