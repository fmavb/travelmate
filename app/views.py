# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse

from django.shortcuts import render
from app.models import Trip
from app.models import UserProfile
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
	if (request.user.is_superuser or request.user.is_anonymous):
		start_dict = {"lat":51.509865,"lng":-0.118092}
		trip_serial = [{"lat":51.509865,"lng":-0.118092, "name":"None"}]
	else:
		userprofile = UserProfile.objects.get(user__exact=request.user)
		start_dict = userprofile.as_dict()
		trip_list = Trip.objects.filter(owner__exact=request.user)
		trip_serial = [ trip.as_dict() for trip in trip_list ]
	compile = {'trips':trip_serial, 'start':start_dict}
	data = json.dumps(compile)
	context_dict = {'json_data': data}
	response = render(request, 'home.html', context_dict)
	return response



def about(request):
	return render(request, 'about.html')



def register(request):
	# A boolean value for telling the template
	# whether the registration was successful.
	# Set to False initially. Code changes value to
	# True when registration succeeds.

	registered = False

	# If it's a HTTP POST, we're interested in processing form data.

	if request.method == 'POST':
		# Attempt to grab information from the raw form information.
		# Note that we make use of both UserForm and UserProfileForm.
		user_form = UserForm(data=request.POST)
		profile_form = UserProfileForm(data=request.POST)
		# If the two forms are valid...

		if user_form.is_valid() and profile_form.is_valid():
			# Save the user's form data to the database.
			user = user_form.save()
			# Now we hash the password with the set_password method.
			# Once hashed, we can update the user object.
			user.set_password(user.password)
			user.save()
			# Now sort out the UserProfile instance.
			# Since we need to set the user attribute ourselves,
			# we set commit=False. This delays saving the model
			# until we're ready to avoid integrity problems.
			profile = profile_form.save(commit=False)
			profile.user = user
			# Did the user provide a profile picture?
			# If so, we need to get it from the input form and
			# put it in the UserProfile model.

			if 'picture' in request.FILES:
				profile.picture = request.FILES['picture']

			# Now we save the UserProfile model instance.
			profile.save()
			# Update our variable to indicate that the template
			# registration was successful.
			registered = True

		else:
			# Invalid form or forms - mistakes or something else?
			# Print problems to the terminal.
			print(user_form.errors, profile_form.errors)

	else:
		# Not a HTTP POST, so we render our form using two ModelForm instances.
		# These forms will be blank, ready for user input.
		user_form = UserForm()
		profile_form = UserProfileForm()

	# Render the template depending on the context.
	return render(request,
				  'register.html',
				  {'user_form': user_form,
				   'profile_form': profile_form,
				   'registered': registered})


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
	form = TripForm()
	if request.method == 'POST':
		form = TripForm(request.POST)
		if form.is_valid():
			trip = form.save(commit=False)
			trip.owner = request.user
			trip.save()
			return home(request)
		else:
			print(form.errors)
	return render(request, 'add_trip.html', {'form': form})

