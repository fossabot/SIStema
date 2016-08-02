from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^compose/', views.compose, name='compose'),
    url(r'^contacts/', views.contacts, name='contacts')
]