# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *

# Create your views here.
def index(request):
	return render(request, 'travel_buddy_app/index.html')

def register(request):
	if request.method == "POST":
		errors = Users.validate(request.POST)
		if errors:
			for tags,error in errors.iteritems():
				messages.error(request, error, extra_tags=tags)
			return redirect('/')
		else:
			users = Users.objects.filter(username = request.POST['username'])
			if len(users) > 0:
				messages.error(request, "Username has already been taken", extra_tags="username")
				return redirect('/')
			else:
				user = Users.objects.create(name = request.POST['name'], username = request.POST['username'], password = request.POST['pass'])
				request.session['user_id'] = user.id
				request.session['user_name'] = user.name
				return redirect('/travels')
def dashboard(request):
	return render(request, 'travel_buddy_app/dashboard.html')

def destination(request, id):
	return render(request, 'travel_buddy_app/destination.html')

def add_form(request):
	return render(request, 'travel_buddy_app/add.html')