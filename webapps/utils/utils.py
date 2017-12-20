from portal.models import *

def is_user_proj_act_permitted(user, project_id, action_type):
	# Check the proj has the action perm
	projects = Project.objects.filter(id=project_id); # Project id is unique
	if len(projects) == 0:
		return (False, 'The requested project does not exist');
	project = projects[0];
	project_perm = project.project_permissions.split(',');
	project_name = project.project_name;
	if not action_type in project_perm:
		return (False, 'The project:%s is not permitted for the action: %s'%(project_name, action_type));
	# Check the user has the project perm
	userwrapper = user.userwrapper;
	this_user_all_userProjRela = UserProjectRelation.objects.filter(user=userwrapper);
	is_user_permitted_for_proj = False;
	tgt_user_proj_rela = None;
	for userProjRela_i in this_user_all_userProjRela:
		if userProjRela_i.project.project_name == project_name:
			is_user_permitted_for_proj = True;
			tgt_user_proj_rela = userProjRela_i;
			break;
	if not is_user_permitted_for_proj:
		return (False, 'You are not permitted for the project:%s'%(project_name));
	# Check the user has the action permitted for the project
	user_this_proj_perm = tgt_user_proj_rela.user_permissions.split(',');
	if not action_type in user_this_proj_perm:
		return (False, 'You are not permitted for the action:%s for the project:%s'%(action_type, project_name));
	# Passed all checks
	return (True, '');