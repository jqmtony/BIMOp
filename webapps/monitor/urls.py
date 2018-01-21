from django.urls import path, re_path
from . import views

urlpatterns = [
	path('<int:project_id>/', views.view3D, name = 'view3D'),
	path('<int:project_id>/sensorsDataQuery/<str:queryType>/<str:sensorType>', views.sensorsDataQuery, name = 'sensorsDataQuery'),
	path('<int:project_id>/sensorsDataQuery/<str:queryType>/<str:sensorType>/<str:guid>/<str:startTime>/<str:endTime>', views.sensorsDataQuery, name = 'sensorsDataQuery'),

	]