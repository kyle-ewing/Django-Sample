from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^dashboard$', views.dash),
    url(r'^process_reg$', views.process_reg),
    url(r'^process_login$', views.process_log),
    url(r'^logout$', views.logout),
    url(r'^new$', views.new),
    url(r'^process_new$', views.process_new),
    url(r'^trips/(?P<number>\d+)$', views.trip),
    url(r'^remove/(?P<number>\d+)$', views.remove),
    url(r'^trips/edit/(?P<number>\d+)$', views.edit),
    url(r'^process_edit/(?P<number>\d+)$', views.process_edit),
    url(r'^join/(?P<number>\d+)$', views.join),
    url(r'^cancel/(?P<number>\d+)$', views.cancel),
]
