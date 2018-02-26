from django.conf.urls import url
from . import views

urlpatterns = [
    # show registration page
    url(r'^registration$', views.registration),
    # action register
    url(r'^register$', views.register),
    # show login page
    url(r'^login$', views.login),
    # action login
    url(r'^processLogin$', views.login),
    # show edit page
    url(r'^edit$', views.edit_page),
    # action edit 
    url(r'^update$', views.edit),
    # logout
    url(r'^logout$', views.logout),
    # show 
    url(r'^show$', views.show),
]