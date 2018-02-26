from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^show$', views.show),
    url(r'^update/(?P<product_id>\d+)$', views.update),
    url(r'^delete/(?P<product_id>\d+)$', views.delete),
]