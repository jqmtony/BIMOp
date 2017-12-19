from django.urls import path, re_path
from django.contrib.auth.views import login, logout_then_login
from . import views

urlpatterns = [
	re_path(r'^login$', login, {'template_name': 'portal/html/login.html'}, name = 'login', ),
	re_path(r'^logout$', logout_then_login, {'login_url': login}, name = 'logout_then_login'),
	path(r'', views.home, name = 'home'),
	re_path(r'^admin$', views.admin, name = 'admin'),
	re_path(r'^dashboard', views.dashboard, name = 'dashboard')
	]