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
	errors.append(perm_check[1]);
	if perm_check[0]:
		pass;
	return render(request, 'monitor/html/view3D.html', {'errors': errors,
														});

