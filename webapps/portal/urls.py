from django.urls import path

from . import views

urlpatterns = ['',
	path(r'^login$', 'django.contrib.auth.views.login'),
	path(r'^logout', 'django.contrib.auth.views.logout_then_login'),
	path(r'', views.home, name = 'home'),
	]