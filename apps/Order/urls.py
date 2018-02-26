from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^checkout$', views.checkout),
    url(r'^processPayment$', views.processPayment),
    url(r'^show$', views.show),
]
