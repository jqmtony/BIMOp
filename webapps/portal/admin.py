from django.contrib import admin

from .models import *

admin.site.register([UserWrapper, Project, UserProjectRelation])