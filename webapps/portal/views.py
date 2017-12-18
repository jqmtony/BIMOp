from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate

from portal.models import *

@login_required
def dashboard(request):
	projects = Project.objects.filter(user = request.user)
	return render(request, 'portal/html/dashboard.html', {'projects': projects})

def home(request):
	return render(request, 'portal/html/index.html')


