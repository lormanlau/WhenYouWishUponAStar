# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
def index(request):
	return render(request, 'travel_buddy_app/index.html')

def dashboard(request):
	return render(request, 'travel_buddy_app/dashboard.html')

def destination(request, id):
	return render(request, 'travel_buddy_app/destination.html')

def add_form(request):
	return render(request, 'travel_buddy_app/add.html')