# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from app.models import Trip
from app.models import UserProfile
from app.forms import *
from django.contrib.auth.models import User
import json



# user auth


from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from app.forms import TripForm

from datetime import datetime

# Create your views here.
def home(request):
	# Check if User is Admin or Anonymous
	# If yes, we use hardcoded values
	# If a registered non-admin user, we fetch their trips
	# Finally we dump whatever we have into JSON
	if(request.user.is_superuser or request.user.is_anonymous):
		start_dict = {"lat":51.509865,"lng":-0.118092}
		trip_serial = [{"lat":51.509865,"lng":-0.118092, "name":"None"}]
	else:
		try:
			userprofile = UserProfile.objects.get(user__exact=request.user)
		except UserProfile.DoesNotExist:
			return HttpResponseRedirect("/app/settings/")
		start_dict = userprofile.as_dict()
		trip_list = Trip.objects.filter(owner__exact=request.user)
		trip_serial = [ trip.as_dict() for trip in trip_list ]
	compile = {'trips':trip_serial, 'start':start_dict}
	data = json.dumps(compile)
	context_dict = {'json_data': data}
	response = render(request, 'home.html', context_dict)
	return response



def about(request):
	request = render(request,'about.html',{})
	return request

def contact(request):
	return HttpResponse("Work in progress...")

def pop_trips(request):
	return HttpResponse("Work in progress...")

def recent_trips(request):
	trips = Trip.objects.order_by('startDate')
	context_dict = {'trips':trips}
	return render(request,'recent_trips.html',context_dict)

def welltrav_travellers(request):
	return HttpResponse("Work in progress...")

def most_active_travellers(request):
	return HttpResponse("Work in progress...")

@login_required
def passport(request):

	destinations = Trip.objects.filter(owner=request.user).order_by('destination')
	context_dict = {'destinations':destinations}
	return render(request,'passport.html',context_dict)

@login_required
def settings(request):
	# Create an array of all our destinations,
	# and then dump into json so we can pass it on to settings.html for autocomplete
	# Ordered by alphabetical order
	
	# Ordered by alphabetical order
	dest = [destination.name for destination in Destination.objects.all().order_by('name')]
	compile = {'names': dest}
	data = json.dumps(compile)

	# Check if UserProfile already exists, if it does we just update it with relevant changes.
	try:
		profile = request.user.userprofile
	except UserProfile.DoesNotExist:
		profile = UserProfile(user=request.user)
	if request.method == 'POST':
		form = Settings(request.POST,instance=profile)
		# Set up values from form
		if form.is_valid():
			profile = form.save(commit=False)
			profile.user = request.user
			# AutoComplete works with TextInput, therefore we match a valid text input to Destination entity
			# Form Validation happens in JavaScript, only valid result accepted onSubmit
			homeCountryText = form.cleaned_data['homeCountryText']
			destinationObject = Destination.objects.get(name__exact=homeCountryText)
			profile.homeCountry = destinationObject
			profile.save()
			return home(request)
		else:
			print (form.errors)
	else:
		form = Settings(instance=profile)

	request = render(request,'settings.html',{'form': form, 'json_data': data})
	return request


def user_login(request):
	# If the request is a HTTP POST, try to pull out the relevant information.
	if request.method == 'POST':

		# Gather the username and password provided by the user.
		# This information is obtained from the login form.
		# We use request.POST.get('<variable>') as opposed
		# to request.POST['<variable>'], because the
		# request.POST.get('<variable>') returns None if the
		# value does not exist, while request.POST['<variable>']
		# will raise a KeyError exception.
		username = request.POST.get('username')
		password = request.POST.get('password')
		# Use Django's machinery to attempt to see if the username/password
		# combination is valid - a User object is returned if it is.
		user = authenticate(username=username, password=password)
		# If we have a User object, the details are correct.
		# If None (Python's way of representing the absence of a value), no user
		# with matching credentials was found.

		if user:
			# Is the account active? It could have been disabled.

			if user.is_active:
				# If the account is valid and active, we can log the user in.
				# We'll send the user back to the homepage.
				login(request, user)
				return HttpResponseRedirect(reverse('home'))

			else:
				# An inactive account was used - no logging in!
				return HttpResponse("Your TravelMate account is disabled.")

		else:
			# Bad login details were provided. So we can't log the user in.
			print("Invalid login details: {0}, {1}".format(username, password))
			return HttpResponse("Invalid login details supplied.")
			# The request is not a HTTP POST, so display the login form.
			# This scenario would most likely be a HTTP GET.

	else:
		# No context variables to pass to the template system, hence the
		# blank dictionary object...
		return render(request, 'registration/login.html', {})




# Use the login_required() decorator to ensure only those logged in can
# access the view.
@login_required
def user_logout(request):
	# Since we know the user is logged in, we can now just log them out.
	logout(request)
	# Take the user back to the homepage.
	return HttpResponseRedirect(reverse('home'))

@login_required
def add_trip(request):
	# Create an array of all our destinations,
	# and then dump into json so we can pass it on to settings.html for autocomplete
	# Ordered by alphabetical order
	dest = [destination.name for destination in Destination.objects.all().order_by('name')]
	compile = {'names': dest}
	data = json.dumps(compile)

	form = TripForm()
	if request.method == 'POST':
		form = TripForm(request.POST)
		if form.is_valid():
			trip = form.save(commit=False)
			trip.owner = request.user
			# AutoComplete works with TextInput, therefore we match a valid text input to Destination entity
			# Form Validation happens in JavaScript, only valid result accepted onSubmit
			destinationText = form.cleaned_data['destinationText']
			destinationObject = Destination.objects.get(name__exact=destinationText)
			trip.destination = destinationObject
			trip.save()
			return home(request)
		else:
			print(form.errors)
	return render(request, 'add_trip.html', {'form': form, 'json_data': data})

@login_required
def trips(request):
	trips = Trip.objects.filter(owner__exact=request.user).order_by('startDate')
	context_dict = {'trips':trips}
	return render(request,'trips.html',context_dict)

@login_required
def view_profile(request):
	return HttpResponse("Work in progress...")

