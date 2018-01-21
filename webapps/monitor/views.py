from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required

from .models import *
from portal.models import *
from utils.utils import is_user_proj_act_permitted
from utils.databaseCode import *
from utils.BIMServerRequests import getLoginRequest

import requests
import json

@login_required
def view3D(request, project_id):
	user = request.user;
	perm_check = is_user_proj_act_permitted(user, project_id, MONITOR)
	errors = {};
	bim_server_ip = None;
	bim_server_port = None;
	bim_server_username = None;
	bim_server_password = None;
	bim_server_poid = None;
	if perm_check[0]:
		tgtproject = Project.objects.filter(id=project_id)[0];
		bim_server_ip = tgtproject.bim_server_ip;
		bim_server_port = tgtproject.bim_server_port;
		bim_server_username = tgtproject.bim_server_username;
		bim_server_password = tgtproject.bim_server_password;
		sensor_data_update_interval_ms = tgtproject.sensor_data_update_interval_ms;
		# Get the bimserver token
		bim_server_loginRequest = getLoginRequest(bim_server_username, bim_server_password);
		bim_server_loginReturn = requests.post('http://%s:%s/json'%(bim_server_ip, bim_server_port), 
								 				json = bim_server_loginRequest);
		if bim_server_loginReturn.status_code == 200:
			bim_server_loginReturn_json = json.loads(bim_server_loginReturn.text);
			if 'exception' in bim_server_loginReturn_json['response']:
				bim_server_token = None;
				errors['bimserver_login'] = 'BIM server returns exception %s'%(bim_server_loginReturn_json['response']['exception']);
			else:
				bim_server_token = json.loads(bim_server_loginReturn.text)['response']['result'];
		else:
			bim_server_token = None;
			errors['bimserver_login'] = 'BIM server returns code %s.'%(bim_server_loginReturn.status_code)

		bim_server_poid = tgtproject.bim_server_poid;
		bim_server_roid = tgtproject.bim_server_roid;
		# Get the project component BIM server GUIDs and its available sensors and related units
		bimComponents = BIMComponent.objects.filter(project__id=project_id);
		#project_bim_guids = list(bimComponents.values_list('guid', flat = True));
		project_bim_components_info = {}; # {GUID: {'sensorType': 'unit',
		                                  #         'sensorType': 'unit'}}
		for bimComponent in bimComponents:
			thisCompGUID = bimComponent.guid;
			thisCompSensors = bimComponent.sensor_set.all();
			thisCompSensorsDict = {};
			for thisCompSensor in thisCompSensors:
				thisCompSensorType = thisCompSensor.sensorType;
				thisCompSensorUnit = thisCompSensor.unit;
				thisCompSensorsDict[thisCompSensorType] = thisCompSensorUnit;
			project_bim_components_info[thisCompGUID] = thisCompSensorsDict;

	else:
		errors['authentication'] = perm_check[1];
	return render(request, 'monitor/html/view3D.html', {'errors': errors,
														'bim_server_ip': bim_server_ip,
														'bim_server_port': bim_server_port,
														'bim_server_token': bim_server_token,
														'bim_server_poid': bim_server_poid,
														'bim_server_roid': bim_server_roid,
														'project_bim_components_info': project_bim_components_info,
														'project_id': project_id,
														'sensor_data_update_interval_ms': sensor_data_update_interval_ms});


@login_required
def sensorsDataQuery(request, project_id, queryType, sensorType, guid=None, startTime=None, endTime=None, interval=None):
	user = request.user;
	perm_check = is_user_proj_act_permitted(user, project_id, MONITOR)
	errors = {};
	queryResults = [];
	if perm_check[0]:	
		if queryType == 'latestAll':
			project_bim_guids = getProjectBimGuids(project_id);
			relatedSensors = Sensor.objects.filter(measuredTarget__guid__in=project_bim_guids).filter(sensorType=sensorType);
			for relatedSensor in relatedSensors:
				thisGuid = relatedSensor.measuredTarget.guid;
				thisLastestData = SensorDataHist.objects.filter(sensor=relatedSensor).latest('recordedTime');
				thisDataTime = thisLastestData.recordedTime;
				thisDataValue = thisLastestData.value;
				thisDataIsGood = thisLastestData.isGood;
				thisDataIsBadNotes = thisLastestData.isBadNotes;
				thisSensorData = {};
				thisSensorData['guid'] = thisGuid;
				thisSensorData['name'] = str(relatedSensor);
				thisSensorData['recordedTime'] = thisDataTime.isoformat();
				thisSensorData['value'] = thisDataValue;
				thisSensorData['isGood'] = thisDataIsGood;
				thisSensorData['notes'] = thisDataIsBadNotes;
				queryResults.append(thisSensorData);
		elif queryType == 'histSingle':
			project_bim_guid = guid;
			relatedSensor = Sensor.objects.filter(measuredTarget__guid=project_bim_guid).filter(sensorType=sensorType)[0];
			allSensorHistInRange = SensorDataHist.objects.filter(sensor=relatedSensor).\
									filter(recordedTime__gt=startTime).filter(recordedTime__lt=endTime).order_by('recordedTime');
			if interval == None:
				for sensorDataHistSingle in allSensorHistInRange:
					thisSensorData = {};
					thisSensorData['guid'] = project_bim_guid;
					thisSensorData['name'] = str(relatedSensor);
					thisSensorData['recordedTime'] = sensorDataHistSingle.recordedTime.isoformat();
					thisSensorData['value'] = sensorDataHistSingle.value;
					thisSensorData['isGood'] = sensorDataHistSingle.isGood;
					thisSensorData['notes'] = sensorDataHistSingle.isBadNotes;
					queryResults.append(thisSensorData);
	else:
		errors['authentication'] = perm_check[1];
	jsonMap = {'sensorsDataQuery':{'queryType': queryType,
									  'sensorType': sensorType,
									  'project_id': project_id,
									  'queryResults': queryResults},
							 'errors': errors};
			
	return JsonResponse(jsonMap, json_dumps_params={'indent': 2});


def getProjectBimGuids(project_id):
	bimComponents = BIMComponent.objects.filter(project__id=project_id);
	project_bim_guids = list(bimComponents.values_list('guid', flat = True));
	return project_bim_guids;
