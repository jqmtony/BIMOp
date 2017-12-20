from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate

from portal.models import *

@login_required
def dashboard(request):
	this_userwrapper = request.user.userwrapper;
	this_userProjRelations = UserProjectRelation.objects.filter(user=this_userwrapper);
	this_projList_permissions = []; # 2-D list, inner list index 0 is project object, index 1 is permission string
	for userProjRelations_i in this_userProjRelations:
		userThisProjPerm = userProjRelations_i.user_permissions.split(','); # Get user permissions
		thisProj = userProjRelations_i.project;
		thisProjPerm = thisProj.project_permissions.split(',');
		commonPerm = list(set(userThisProjPerm).intersection(thisProjPerm));
		this_projList_permissions.append([thisProj, commonPerm]);
	return render(request, 'portal/html/dashboard.html', {'proj_perm_list': this_projList_permissions,
														  'user': this_userwrapper});

def home(request):
	return render(request, 'portal/html/index.html')

@login_required
def admin(request):
	projects = [];
	users = [];
	errors = [];
	usertype = None;
	# Try to get user type
	try:
		usertype = request.user.userwrapper.user_type;
	except:
		# Note the super user has no userwrapper
		pass;
	if usertype == 'administrator':
		projects = Project.objects.all();
		users = UserWrapper.objects.all();
	else:
		errors.append('You are not authorized to view this page.');
	return render(request, 'portal/html/admin.html', {'projects': projects,
													  'users': users,
													  'errors': errors});





