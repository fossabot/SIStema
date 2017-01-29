from django.conf import urls

from . import views

urlpatterns = [
    urls.url(r'^$', views.sistemize, name='sistemize'),
    urls.url(r'^result$', views.sistemize, name='sistemize-result'),
]
