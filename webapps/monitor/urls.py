from django.urls import path, re_path
from . import views

urlpatterns = [
	path('<int:project_id>/', views.view3D, name = 'view3D'),
	]