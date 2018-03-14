# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from app.models import Trip
from app.models import UserProfile
from app.models import Destination, PostImage
from app.forms import *
from django.contrib.auth.models import User
import json
from operator import itemgetter  
from django.shortcuts import get_object_or_404
from django.conf import settings as psettings


# user auth


from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from app.forms import TripForm
from app.forms import BlogForm, PhotoForm
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


#views for static pages /about, /contact, /terms_of_use, and privacy_policy
def about(request):
	request = render(request,'about.html',{})
	return request

def contact(request):
	request = render(request,'contact.html',{})
	return request

def terms_of_use(request):
	request = render(request,'terms_of_use.html',{})
	return request

def privacy_policy(request):
	request = render(request,'privacy_policy.html',{})
	return request

def pop_trips(request):
	
	trips = Trip.objects.order_by('score').reverse()

	context_dict = {'trips':trips}

	return render(request,'pop_trips.html',context_dict)

# order trips by their start date, in from newest to oldest and return in it in the contect dictionary
def recent_trips(request):
	trips = Trip.objects.order_by('startDate').reverse()
	context_dict = {'trips':trips}
	return render(request,'recent_trips.html',context_dict)

# returns a list of list of users and their corresponding number of trips-pairs, in a descending order (based on the number of trips)
# and puts it into the context dictionary
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

# returns a list of list of users and their corresponding number of blogpost-pairs, in a descending order
# and puts it into the context dictionary
def most_active_travellers(request):

	user_posts={}
	posts = BlogPost.objects.all()

	for post in posts:
		user_posts[post.user] = user_posts.get(post.user,0)+1

	user_list = []
	for key, value in sorted(user_posts.items(), key = itemgetter(1), reverse = True):
		user_list.append([key, value])

	context_dict = {'user_list':user_list}
	return render(request,'most_active_travellers.html',context_dict)

# view for the passport page, context dictionary contains the destinations
@login_required
def passport(request):
	destinations = Trip.objects.filter(owner=request.user).order_by('destination')
	context_dict = {'destinations': destinations}
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
			return HttpResponseRedirect(reverse('view_trip', kwargs={'username': username, 'trip_name_slug': trip_name_slug}))
		else:
			print(form.errors)
	return render(request, 'add_blog_post.html', {'form': form, 'slug':trip_name_slug})

# view for base.html, passes the user object into the context dictionary
def base(request):
	context_dict = {}
	user = get_object_or_404(User, username=request.user)
	context_dict['user'] = user

	return render(request,'base.html',context_dict)

# view for the user profile, context dictionary contains the user, userprofile and the user's trips in reverse chronological order
@login_required
def view_profile(request,username):

	user = get_object_or_404(User, username__exact=username)
	try:
		profile = UserProfile.objects.get(user__exact=user)
	except UserProfile.DoesNotExist:
		return HttpResponseRedirect("/app/settings/")
	trips = Trip.objects.filter(owner=user).order_by('startDate').reverse()
	context_dict = {'user':user, 'trips':trips, 'profile':profile }

	return render(request,'view_profile.html',context_dict)


# view for a given trip. context dictionary gets the trip object (identified by slugified title)
# and the trip's blogposts ordered by in reverse chronological order
def view_trip(request, username, trip_name_slug):
	context_dict = {}

	try:
		trip = Trip.objects.get(slug=trip_name_slug)
		context_dict['trip'] = trip
		posts = BlogPost.objects.filter(trip__exact=trip).order_by('Date').reverse()
		context_dict['posts'] = posts
	except Trip.DoesNotExist:
		context_dict['trip'] = None
		context_dict['posts'] = None
	return render(request, 'trip.html', context_dict)

# context dictionary gets the post and trip identified by their slugified titles
# and the photos of the given post
def blog_post(request, username, trip_name_slug, post_name_slug):
	context_dict = {}
	try:
		post = BlogPost.objects.get(slug=post_name_slug)
		context_dict['post']=post
		trip = Trip.objects.get(slug=trip_name_slug)
		context_dict['trip'] = trip
	except BlogPost.DoesNotExist:
		context_dict['post'] = None
	except Trip.DoesNotExist:
		context_dict['trip'] = None
	photos_list = PostImage.objects.filter(post=post)
	context_dict["photos"] = photos_list

	return render(request, 'blog_post.html', context_dict)

# View that deletes a specific trip
def delete_trip(request,username, trip_name_slug):
	object = Trip.objects.get(slug__exact=trip_name_slug)
	object.delete()
	return HttpResponseRedirect(reverse('view_profile', kwargs={'username': username}))

# View that deletes a specific blog post
def delete_post(request, username, trip_name_slug, post_name_slug):
	object = BlogPost.objects.get(slug__exact=post_name_slug)
	object.delete()
	return HttpResponseRedirect(reverse('view_trip', kwargs={'username': username, 'trip_name_slug': trip_name_slug}))

def upload_images(request, username, trip_name_slug, post_name_slug):
	# Construct the context Dictionary
	context_dict = {}
	try:
		inpost = BlogPost.objects.get(slug=post_name_slug)
		context_dict['post'] = inpost
		trip = Trip.objects.get(slug=trip_name_slug)
		context_dict['trip'] = trip
	except BlogPost.DoesNotExist:
		context_dict['post'] = None
	except Trip.DoesNotExist:
		context_dict['trip'] = None

	if request.method == 'POST':
		# If POST use form to create PostImage object
		form = PhotoForm(request.POST, request.FILES)
		if form.is_valid():
			photo = form.save(commit=False)
			photo.post = inpost
			photo.save()
			# Create a JSON from the new PostImage object, and pass that in as our response, since the JS uses JSON
			data = {'is_valid': True, 'name': photo.name, 'url': photo.image.url}
		else:
			data = {'is_valid': False}
		return JsonResponse(data)
	else:
		# If GET add current post photos to the context dict
		photos_list = PostImage.objects.filter(post=inpost)
		context_dict["photos"] = photos_list
		return render(request, 'upload_images.html', context_dict)

def delete_image(request, username, trip_name_slug, post_name_slug, image_name):
	object = PostImage.objects.get(name__exact=image_name)
	# Remove image from media folder
	os.remove(os.path.join(psettings.MEDIA_ROOT, object.image.name))
	object.delete()
	return HttpResponseRedirect(reverse('upload_images', kwargs={'username': username, 'trip_name_slug': trip_name_slug, 'post_name_slug':post_name_slug}))

def search(request):
	context_dict = {}
	query = request.GET.get('search-bar','')
	if query != '':
		try:
			users = User.objects.filter(username__icontains=query)
			public = []
			if len(users) != 0:
				for user in users:
					userProfile = UserProfile.objects.get(user__exact=user)
				if userProfile.public:
					public.append(user)
				context_dict['public'] = public
				context_dict['login_required'] = users
				return render(request, 'search_users.html',context_dict)
		except User.DoesNotExist:
			return render(request, 'search_users.html')
		except UserProfile.DoesNotExist:
			return render(request, 'search_users.html')

	return render(request, 'search_users.html', context_dict)

