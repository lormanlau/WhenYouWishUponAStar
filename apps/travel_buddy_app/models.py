# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import time

class UserManager(models.Manager):
	def validate(self, user_data):
		errors = {}

		if len(user_data['name']) < 3:
			errors['name'] = "Name can not be less than 3 letters long"
		if len(user_data['username']) < 3:
			errors['username'] = "Username can not be less than 3 letters long"
		if len(user_data['pass']) < 8:
			errors['password'] = "Password must be atleast 8 characters long"
		if user_data['pass'] != user_data['con_pass']:
			errors['password'] = "Passwords must match"

		return errors

class DestinationManager(models.Manager):
	def validate(self, des_data):
		errors = {}
		today = time.strftime("%Y-%m-%d")
		print des_data['from']

		if len(des_data['des_name']) < 1:
			errors['des_name'] = "Destination name can not be empty"
		if len(des_data['desc']) < 1:
			errors['description'] = "Description can not be empty"
		if len(des_data['from']) < 1:
			errors['from'] = "Please enter a from travel date"
		if len(des_data['to']) < 1:
			errors['to'] = "Please enter a to travel date"
		if des_data['from'] < today:
			errors['from'] = "From date should be a future date"
		if des_data['to'] < des_data['from']:
			errors['to'] = "To date should be after your from date"

		return errors

# Create your models here.
class Users(models.Model):
	name = models.CharField( max_length = 255 )
	username = models.CharField( max_length = 255 )
	password = models.CharField( max_length = 255 )
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	objects = UserManager()

class Destinations(models.Model):
	place = models.CharField( max_length = 255 )
	desc = models.TextField()
	travel_from = models.DateField()
	travel_to = models.DateField()
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	user = models.ForeignKey(Users)
	objects = DestinationManager()

class JoinedTravels(models.Model):
	user = models.ForeignKey(Users)
	destination = models.ForeignKey(Destinations)
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
		
		