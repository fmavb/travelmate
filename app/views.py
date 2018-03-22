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
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

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
    if (request.user.is_superuser or request.user.is_anonymous):
        start_dict = {"lat": 51.509865, "lng": -0.118092}
        trip_serial = [{"lat": 51.509865, "lng": -0.118092, "name": "None"}]
    else:
        try:
            userprofile = UserProfile.objects.get(user__exact=request.user)
        except UserProfile.DoesNotExist:
            return HttpResponseRedirect("/app/settings/")
        start_dict = userprofile.as_dict()
        trip_list = Trip.objects.filter(owner__exact=request.user)
        trip_serial = [trip.as_dict() for trip in trip_list]
    compile = {'trips': trip_serial, 'start': start_dict}
    data = json.dumps(compile)
    context_dict = {'json_data': data}
    context_dict['previous'] = request.META.get('HTTP_REFERER')
    response = render(request, 'app/home.html', context_dict)
    return response


# views for static pages /about, /contact, /terms_of_use, and privacy_policy
def about(request):
    request = render(request, 'app/about.html', {})
    return request


def contact(request):
    request = render(request, 'app/contact.html', {})
    return request


def terms_of_use(request):
    request = render(request, 'app/terms_of_use.html', {})
    return request


def privacy_policy(request):
    request = render(request, 'app/privacy_policy.html', {})
    return request


# helper function: returns a dictionary with paginatored value
def paginatored(l, request):
    page = request.GET.get('page', 1)
    paginator = Paginator(l, 10)

    try:
        elems = paginator.page(page)
    except PageNotAnInteger:
        elems = paginator.page(1)
    except EmptyPage:
        elems = paginator.page(paginator.num_pages)

    return {'elems': elems}


# view for the most popular trips
# context dictionary gets the list of trips ordered by their scores (highest score first, lowest last)
def pop_trips(request):
    trips_list = Trip.objects.order_by('score').reverse()
    context_dict = paginatored(trips_list, request)
    return render(request, 'app/pop_trips.html', context_dict)


# order trips by their start date, from newest to oldest and return in it in the context dictionary
def recent_trips(request):
    trips_list = Trip.objects.order_by('startDate').reverse()
    context_dict = paginatored(trips_list, request)
    return render(request, 'app/recent_trips.html', context_dict)


# helper function: takes in a dictionary
# returns a list of list of the key-value pairs ordered by the values (descending)
def sort_dict(d):
    user_list = []
    for key, value in sorted(d.items(), key=itemgetter(1), reverse=True):
        user_list.append([key, value])
    return user_list


# view for the best travelled users: context dictionary gets a list of list of users and their corresponding number of trips
# in descending order
def best_travelled(request):
    trips = Trip.objects.all()
    user_trips = {}
    for trip in trips:
        user_trips[trip.owner] = user_trips.get(trip.owner, 0) + 1

    context_dict = paginatored(sort_dict(user_trips), request)
    return render(request, 'app/best_travelled.html', context_dict)


# view for the best travelled users: context dictionary gets a list of list of users and their corresponding blogposts
# in descending order
def most_active_travellers(request):
    user_posts = {}
    posts = BlogPost.objects.all()

    for post in posts:
        user_posts[post.user] = user_posts.get(post.user, 0) + 1

    context_dict = paginatored(sort_dict(user_posts), request)
    return render(request, 'app/most_active_travellers.html', context_dict)


# view for the passport page, context dictionary contains the destinations
@login_required
def passport(request):
    trips = Trip.objects.filter(owner=request.user).order_by('destination')
    output = []
    # Checking for duplicate destinations
    for trip in trips:
        unique = True
        for elt in output:
            if trip.destination == elt.destination:
                unique = False
                break
        if unique:
            output.append(trip)

    destinations = Destination.objects.all()
    numDestinations = int((len(trips) / len(destinations)) * 100)
    context_dict = {'trips': output, 'num_destinations': numDestinations}
    return render(request, 'app/passport.html', context_dict)


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
    compile = {'names': dest, 'hc': hc, 'public': pub}
    data = json.dumps(compile)

    if request.method == 'POST':
        form = Settings(request.POST, request.FILES, instance=profile)
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

    request = render(request, 'app/settings.html',
                     {'form': form, 'json_data': data, 'previous': request.META.get('HTTP_REFERER')})
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
            trip.save()
            # Use Redirect so that URL in browser also changes
            return HttpResponseRedirect(reverse('home'))
        else:
            print(form.errors)
    return render(request, 'app/add_trip.html', {'form': form, 'json_data': data})


@login_required
def add_blog_post(request, username, trip_name_slug):
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
            return HttpResponseRedirect(
                reverse('view_trip', kwargs={'username': username, 'trip_name_slug': trip_name_slug}))
        else:
            print(form.errors)
    return render(request, 'app/add_blog_post.html', {'form': form, 'slug': trip_name_slug})


# view for base.html, passes the user object into the context dictionary
def base(request):
    context_dict = {}
    user = get_object_or_404(User, username=request.user)
    context_dict['user'] = user

    return render(request, 'app/base.html', context_dict)


# view for the user profile, context dictionary contains the user, userprofile and the user's trips in reverse chronological order
def view_profile(request, username):
    user = get_object_or_404(User,username=username)
    userPublic = UserProfile.objects.get(user=user)
    userPublic = userPublic.public
    if userPublic == False and request.user.is_authenticated == False:
        return HttpResponseRedirect('/login/')

    user = get_object_or_404(User, username__exact=username)
    try:
        profile = UserProfile.objects.get(user__exact=user)
    except UserProfile.DoesNotExist:
        return HttpResponseRedirect("/app/settings/")
    trips_list = Trip.objects.filter(owner=user).order_by('startDate').reverse()
    context_dict = paginatored(trips_list, request)
    context_dict['user'] = user
    context_dict['profile'] = profile

    return render(request, 'app/view_profile.html', context_dict)


# view for a given trip. context dictionary gets the trip object (identified by slugified title)
# and the trip's blogposts ordered by in reverse chronological order
def view_trip(request, username, trip_name_slug):
    context_dict = {}
    user = get_object_or_404(User, username=username)
    userPublic = UserProfile.objects.get(user=user)
    userPublic = userPublic.public
    if userPublic == False and request.user.is_authenticated == False:
        return HttpResponseRedirect('/login/')
    try:
        trip = Trip.objects.get(slug=trip_name_slug)
        posts = BlogPost.objects.filter(trip__exact=trip).order_by('Date').reverse()
        context_dict = paginatored(posts, request)
        context_dict['trip'] = trip
        stringscore = "o"*trip.score
        context_dict['score'] = stringscore
        ratingIN = []
        if (not request.user.is_anonymous):
            ratingIN = Rating.objects.filter(trip__exact=trip, owner=request.user)
        if(ratingIN.__len__() is not 0):
            stringrating = "o"*ratingIN[0].score
        else:
            stringrating = ""
        context_dict['rating'] = stringrating
        comments = {}
        for post in posts:
            c = Comment.objects.filter(post=post).count()
            comments[post.title] = c
        context_dict['comments'] = comments
    except Trip.DoesNotExist:
        context_dict['trip'] = None
    except BlogPost.DoesNotExist:
        context_dict['elems'] = None

    return render(request, 'app/trip.html', context_dict)


# context dictionary gets the post and trip identified by their slugified titles
# and the photos of the given post
def blog_post(request, username, trip_name_slug, post_name_slug):
    # Had to remove the context_dict, it was interfering with the form
    try:
        post = BlogPost.objects.get(slug=post_name_slug)
        trip = Trip.objects.get(slug=trip_name_slug)
    except BlogPost.DoesNotExist:
        post = None
    except Trip.DoesNotExist:
        trip = None
    photos_list = PostImage.objects.filter(post=post)
    comments = Comment.objects.filter(post=post)

    return render(request, 'app/blog_post.html',
                  {'post': post, 'trip': trip, 'photos': photos_list, 'comments': comments})


# View that deletes a specific trip
def delete_trip(request, username, trip_name_slug):
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
        return render(request, 'app/upload_images.html', context_dict)


def delete_image(request, username, trip_name_slug, post_name_slug, image_name):
    object = PostImage.objects.get(name__exact=image_name, post__slug__exact=post_name_slug)
    # Remove image from media folder
    os.remove(os.path.join(psettings.MEDIA_ROOT, object.image.name))
    object.delete()
    return HttpResponseRedirect(reverse('upload_images', kwargs={'username': username, 'trip_name_slug': trip_name_slug,
                                                                 'post_name_slug': post_name_slug}))


# helper function: returns a dictionary with paginatored value
def paginatored_log_req(l, request):
    page = request.GET.get('page', 1)
    paginator = Paginator(l, 10)

    try:
        login_required = paginator.page(page)
    except PageNotAnInteger:
        login_required = paginator.page(1)
    except EmptyPage:
        login_required = paginator.page(paginator.num_pages)

    return {'login_required': login_required}


def search(request):
    query = request.GET.get('search-bar', '')

    users = UserProfile.objects.filter(user__username__icontains=query)
    context_dict = paginatored_log_req(users, request)

    return render(request, 'app/search_users.html', context_dict)


@login_required
def like_trip(request):
    tripslug = None
    rating = None
    if request.method == 'GET':
        tripslug = request.GET['slug']
        rating = int(request.GET['rating'])
    score = 0
    if tripslug:
        trip = Trip.objects.get(slug=tripslug)
        if trip:
            r = Rating(score=rating, owner=request.user, trip=trip)
            r.save()
            if trip.score == 0:
                score = rating
            else:
                score = (int(trip.score) + rating) // 2

    return HttpResponse(int(score))


@login_required
def comment(request):
    comment = request.POST.get('comment', None)
    postslug = request.POST.get('slug', None)

    c = None
    if postslug and comment:
        post = BlogPost.objects.get(slug=postslug)
        c = Comment(Date=datetime.today(), content=comment, user=request.user, post=post)
        c.save()

    return JsonResponse(c.as_dict())


@login_required
def edit_trip(request, username, trip_name_slug):
    dest = [destination.name for destination in Destination.objects.all().order_by('name')]
    trip = Trip.objects.get(slug=trip_name_slug)
    compile = {'names': dest, 'trip': trip.as_dict(), 'public': trip.public}
    data = json.dumps(compile)
    form = TripForm()
    if request.method == 'POST':
        form = TripForm(request.POST)
        if form.is_valid():
            # AutoComplete works with TextInput, therefore we match a valid text input to Destination entity
            # Form Validation happens in JavaScript, only valid result accepted onSubmit
            destinationText = form.cleaned_data['destinationText']
            destinationObject = Destination.objects.get(name__exact=destinationText)
            trip.destination = destinationObject
            trip.title = form.cleaned_data['title']
            trip.startDate = form.cleaned_data['startDate']
            trip.endDate = form.cleaned_data['endDate']
            trip.save()
            # Use Redirect so that URL in browser also changes
            return HttpResponseRedirect(reverse('view_profile', kwargs={'username': trip.owner}))
        else:
            print(form.errors)
    return render(request, 'app/edit_trip.html', {'form': form, 'json_data': data, 'slug': trip.slug})


@login_required
def edit_post(request, username, trip_name_slug, post_name_slug):
    blog = BlogPost.objects.get(slug=post_name_slug)
    compile = {'post': blog.as_dict()}
    data = json.dumps(compile)
    form = BlogForm()
    if request.method == 'POST':
        form = BlogForm(request.POST)
        if form.is_valid():
            blog.title = form.cleaned_data['title']
            blog.content = form.cleaned_data['content']
            blog.save()
            # Use Redirect so that URL in browser also changes
            return HttpResponseRedirect(
                reverse('view_trip', kwargs={'username': username, 'trip_name_slug': trip_name_slug}))
        else:
            print(form.errors)
    return render(request, 'app/edit_post.html',
                  {'json_data': data, 'form': form, 'tripslug': trip_name_slug, 'postslug': post_name_slug})
