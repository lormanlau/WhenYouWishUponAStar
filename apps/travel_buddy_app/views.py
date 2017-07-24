# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt

# Create your views here.
def index(request):
	try:
		request.session['user_id']
	except:
		request.session['user_id'] = 0
	if request.session['user_id'] != 0:
		return redirect('/travels')
	return render(request, 'travel_buddy_app/index.html')

def register(request):
	if request.method == "POST":
		errors = Users.objects.validate(request.POST)
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
				hashed_pass = bcrypt.hashpw(request.POST['pass'].encode(), bcrypt.gensalt())
				user = Users.objects.create(name = request.POST['name'], username = request.POST['username'], password = hashed_pass)
				request.session['user_id'] = user.id
				request.session['user_name'] = user.name
				return redirect('/travels')

def login(request):
	if request.method == "POST":
		users = Users.objects.filter(username = request.POST['username'])
		if len(users) == 0:
			messages.error(request, "No user found")
			return redirect('/')
		else:
			user = users.first()
			if not bcrypt.checkpw(request.POST['pass'].encode(), user.password.encode()):
				messages.error(request, "Invalid username or Password")
				return redirect('/')
			else:
				request.session['user_id'] = user.id
				request.session['user_name'] = user.name
				return redirect('/travels')

def logout(request):
	request.session['user_id'] = 0
	request.session['user_name'] = None
	return redirect('/')

def dashboard(request):
	try:
		request.session['user_id']
	except:
		request.session['user_id'] = 0
	if request.session['user_id'] == 0:
		messages.error(request, "You are not logged in", extra_tags="login")
		return redirect('/')
	context = {
		'other_places': Destinations.objects.all().exclude(joinedtravels__user__id = request.session['user_id']),
		'my_places': JoinedTravels.objects.filter(user__id = request.session['user_id'])
	}
	return render(request, 'travel_buddy_app/dashboard.html', context)

def destination(request, id):
	context = {
	'place': Destinations.objects.get(id = id),
	'users': JoinedTravels.objects.filter(destination = Destinations.objects.get(id = id))
	}
	return render(request, 'travel_buddy_app/destination.html', context)

def join(request, id):
	JoinedTravels.objects.create(user = Users.objects.get(id = request.session['user_id']), destination = Destinations.objects.get(id = id))
	return redirect('/')

def add_form(request):
	return render(request, 'travel_buddy_app/add.html')

def add(request):
	if request.method == "POST":
		errors = Destinations.objects.validate(request.POST)
		if errors:
			for tags,error in errors.iteritems():
				messages.error(request, error, extra_tags=tags)
			return redirect('/travels/add')
		else:
			place = Destinations.objects.create(place = request.POST['des_name'], desc = request.POST['desc'], travel_from = request.POST['from'], travel_to = request.POST['to'], user = Users.objects.get(id = request.session['user_id']))
			JoinedTravels.objects.create(user = Users.objects.get(id = request.session['user_id']), destination = place)
			return redirect('/travels')





