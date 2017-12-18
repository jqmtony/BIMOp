from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
	project_name = models.CharField(max_length=200)
	user = models.ForeignKey(User, on_delete = models.PROTECT);
	def __str__(self):
		return self.project_name;


