from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index),
	url(r'^travels$', views.dashboard),
	url(r'^travels/destination/(?P<id>\d+)$', views.destination),
	url(r'^travels/add$', views.add_form),
]