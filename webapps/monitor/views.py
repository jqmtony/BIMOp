from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from portal.models import *
from utils.utils import is_user_proj_act_permitted
from utils.code import *

@login_required
def view3D(request, project_id):
	user = request.user;
	perm_check = is_user_proj_act_permitted(user, project_id, MONITOR)
	errors = [];
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
		bim_server_poid = tgtproject.bim_server_poid;
	else:
		errors.append(perm_check[1]);
	return render(request, 'monitor/html/view3D.html', {'errors': errors,
														'bim_server_ip': bim_server_ip,
														'bim_server_port': bim_server_port,
														'bim_server_username': bim_server_username,
														'bim_server_password': bim_server_password,
														'bim_server_poid': bim_server_poid});

