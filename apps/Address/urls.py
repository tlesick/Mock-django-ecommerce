from django.conf.urls import url
from . import views
# Address URLS
urlpatterns = [
    # registration page for address
    url(r'^registration$', views.registration),
    # register an address
    url(r'^register$', views.register),
    # edit an address
    url(r'^edit/(?P<address_id>\d+)$', views.edit),
    # update the address 
    url(r'^update/(?P<address_id>\d+)$', views.update),
    # change preference
    url(r'^preference/(?P<address_id>\d+)$', views.preference_change),

]