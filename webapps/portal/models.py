from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Project(models.Model):
	project_name = models.CharField(max_length=200)
	project_permissions = models.CharField(max_length=200, null = True) # Comma separated string
	bim_server_ip = models.GenericIPAddressField(null = True)
	bim_server_username = models.CharField(max_length=200, null = True)
	bim_server_password = models.CharField(max_length=200, null = True)

	def __str__(self):
		return self.project_name;

class UserWrapper(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	user_type = models.CharField(max_length=200)

	def __str__(self):
		return self.user.username;

class UserProjectRelation(models.Model):
	user = models.ForeignKey(UserWrapper, on_delete=models.CASCADE)
	project = models.ForeignKey(Project, on_delete=models.CASCADE)
	user_permissions = models.CharField(max_length=200)

	def __str__(self):
		return self.user.user.username + '_' + self.project.project_name + '_relation'


"""
Link UserWrapper with User
"""
@receiver(post_save, sender = User)
def create_user_profile(sender, instance, created, **kwargs):
	if created:
		UserWrapper.objects.create(user = instance)
	try:
		instance.userwrapper.save()
	except:
		pass;

#@receiver(post_save, sender = User)
#def save_user_profile(sender, instance, **kwargs):
#	instance.userwrapper.save()