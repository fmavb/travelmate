# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from app.models import Trip
from app.models import UserProfile
from app.models import Destination
from app.forms import *
from django.contrib.auth.models import User
import json
from operator import itemgetter  
from django.shortcuts import get_object_or_404


# user auth


from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from app.forms import TripForm
from app.forms import BlogForm
from datetime import datetime

# Create your views here.
def home(request):
	# Check if User is Admin or Anonymous
	# If yes, we use hardcoded values (LatLng of UK)
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
	trips = Trip.objects.order_by('endDate')

	context_dict = {'trips':trips}

	return render(request,'recent_trips.html',context_dict)

def best_travelled(request):
	trips = Trip.objects.all()

	user_trips={}
	for trip in trips:
		user_trips[trip.owner] = user_trips.get(trip.owner,0)+1

	user_list = []
	for key, value in sorted(user_trips.items(), key = itemgetter(1), reverse = True):
		user_list.append([key, value])

	
	context_dict = {'user_list':user_list}
	return render(request,'best_travelled.html',context_dict)

def most_active_travellers(request):
	

	return HttpResponse("Work in progress...")

@login_required
def passport(request):
	destinations = Trip.objects.filter(owner=request.user).order_by('destination')
	context_dict = {'destinations':destinations}
	return render(request,'passport.html',context_dict)

@login_required
def settings(request):
	# Check if UserProfile already exists, if it does we just update it with relevant changes.
	hc = ""
	pub = False
	try:
		profile = request.user.userprofile
		hc = profile.homeCountry.name
		pub = profile.public
	except UserProfile.DoesNotExist:
		profile = UserProfile(user=request.user)

	# Create an array of all our destinations,
	# and then dump into json so we can pass it on to settings.html for autocomplete
	# Ordered by alphabetical order

	# Ordered by alphabetical order
	dest = [destination.name for destination in Destination.objects.all().order_by('name')]
	compile = {'names': dest, 'hc':hc,'public':pub}
	data = json.dumps(compile)

	if request.method == 'POST':
		form = Settings(request.POST, request.FILES,instance=profile)
		# Set up values from form
		if form.is_valid():
			profile = form.save(commit=False)
			profile.user = request.user
			# AutoComplete works with TextInput, therefore we match a valid text input to Destination entity
			# Form Validation happens in JavaScript, only valid result accepted onSubmit
			homeCountryText = form.cleaned_data['homeCountryText']
			destinationObject = Destination.objects.get(name__exact=homeCountryText)
			profile.homeCountry = destinationObject
			profile.public = form.cleaned_data['public']
			profile.save()
			# Use Redirect so that URL in browser also changes
			return HttpResponseRedirect(reverse('home'))
		else:
			print (form.errors)
	else:
		form = Settings(instance=profile)

	request = render(request,'settings.html',{'form': form, 'json_data': data})
	return request


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
			trip.public = form.cleaned_data['public']
			trip.save()
			# Use Redirect so that URL in browser also changes
			return HttpResponseRedirect(reverse('home'))
		else:
			print(form.errors)
	return render(request, 'add_trip.html', {'form': form, 'json_data': data})

@login_required
def add_blog_post(request, username,trip_name_slug):
	form = BlogForm()
	if request.method == 'POST':
		form = BlogForm(request.POST)
		if form.is_valid():
			blog = form.save(commit=False)
			blog.user = request.user
			blog.Date = datetime.today()
			trip = get_object_or_404(Trip, slug__exact=trip_name_slug)
			blog.trip = trip
			blog.save()
			# Use Redirect so that URL in browser also changes
			return HttpResponseRedirect(reverse('view_trip', request.user.username,trip_name_slug))
		else:
			print(form.errors)
	return render(request, 'add_blog_post.html', {'form': form, 'slug':trip_name_slug})

@login_required
def my_trips(request):
	trips = Trip.objects.filter(owner__exact=request.user).order_by('startDate')
	context_dict = {'trips':trips}
	return render(request,'trips.html',context_dict)

def base(request):
	context_dict = {}
	user = get_object_or_404(User, username=request.user)
	context_dict['user'] = user

	return render(request,'base.html',context_dict)


@login_required
def view_profile(request,username):

	user = get_object_or_404(User, username__exact=username)
	profile = get_object_or_404(UserProfile, user__exact=user)
	trips = Trip.objects.filter(owner=user).order_by('startDate').reverse()
	context_dict = {'user':user, 'trips':trips, 'profile':profile }

	return render(request,'view_profile.html',context_dict)



def view_trip(request, username, trip_name_slug):
	context_dict = {}

	try:
		trip = Trip.objects.get(slug=trip_name_slug)
		context_dict['trip'] = trip
		posts = BlogPost.objects.filter(trip__exact=trip).order_by('Date')
		context_dict['posts'] = posts
	except Trip.DoesNotExist:
		context_dict['trip'] = None
		context_dict['posts'] = None
	return render(request, 'trip.html', context_dict)