from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from portal.models import *
from utils.utils import is_user_proj_act_permitted
from utils.code import *
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
	else:
		errors.append(perm_check[1]);
	return render(request, 'monitor/html/view3D.html', {'errors': errors,
														'bim_server_ip': bim_server_ip,
														'bim_server_port': bim_server_port,
														'bim_server_token': bim_server_token,
														'bim_server_poid': bim_server_poid});

