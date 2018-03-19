
import os, shutil
from datetime import datetime

from django.core.files.images import ImageFile
from django.core.management import execute_from_command_line

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                        'travelmate.settings')

import django
django.setup()
import random
import csv
from django.contrib.auth.models import User
from app.models import Destination, UserProfile, Trip, BlogPost, Comment, Rating

def auto_migrations():
	os.environ.setdefault("DJANGO_SETTINGS_MODULE", "travelmate.settings")
	try:
		from django.core.management import execute_from_command_line
	except ImportError:
		# The above import may fail for some other reason. Ensure that the
		# issue is really that Django is missing to avoid masking other
		# exceptions on Python 2.
		try:
			import django
		except ImportError:
			raise ImportError(
				"Couldn't import Django. Are you sure it's installed and "
				"available on your PYTHONPATH environment variable? Did you "
				"forget to activate a virtual environment?"
			)
		raise
	execute_from_command_line(['manage.py', 'makemigrations', 'app'])
	execute_from_command_line(['manage.py', 'migrate', 'app'])
	execute_from_command_line(['manage.py', 'migrate'])


def clear_media():
	folder = 'media\\flags'
	for file in os.listdir(folder):
		file_path = os.path.join(folder, file)
		try:
			if os.path.isfile(file_path):
				if(".gitkeep" not in file_path):
					os.unlink(file_path)
		except Exception as e:
			print(e)

users = {"john_test":"United Kingdom", "maria_test":"Hungary", "alex_test":"Slovakia", "bob_test":"Turkey", "peter_test":"Argentina",
         "tarzan_test":"United States - California", "cicero_test": "Italy", "julius_test":"Italy", "tom_test":"Switzerland", "ben_test":"Japan",
         "brutus_test":"Australia", "mike_test":"South Africa", "vercingetorix":"France",}

trips = [
	{"owner" : "john_test", "title": "Trip to New Zealand", "destination":"New Zealand", "sdate": "2018-02-24", "edate": "2018-02-28"},
	{"owner" : "john_test", "title": "City Break in Wien", "destination":"Austria", "sdate": "2018-03-11", "edate": "2018-03-13"},
	{"owner" : "bob_test", "title": "Exploring the East", "destination":"China", "sdate": "2017-03-11", "edate": "2017-04-13"},
	{"owner" : "cicero_test", "title": "My Exile", "destination":"Greece", "sdate": "2017-12-11", "edate": "2017-12-24"},
	{"owner" : "julius_test", "title": "Checking out Alesia", "destination":"France", "sdate": "2017-09-01", "edate": "2017-09-30"},
	{"owner" : "brutus_test", "title": "Papa don't Preach", "destination":"Italy", "sdate": "2015-03-15", "edate": "2015-03-15"},
	{"owner" : "tarzan_test", "title": "Welcome to the Jungle", "destination":"Zimbabwe", "sdate": "2014-06-24", "edate": "2015-02-28"},
	{"owner" : "alex_test", "title": "Skiing in Canada", "destination":"Canada", "sdate": "2017-12-11", "edate": "2017-12-28"},
	{"owner" : "alex_test", "title": "Such History", "destination":"Italy", "sdate": "2017-08-29", "edate": "2017-09-10"},
	{"owner" : "alex_test", "title": "Balaton Time", "destination":"Hungary", "sdate": "2015-07-11", "edate": "2015-07-13"},
	{"owner" : "mike_test", "title": "Trip to Swaziland", "destination":"Swaziland", "sdate": "2015-07-15", "edate": "2015-08-01"},
]

lorem = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec elementum nisl turpis, vel feugiat enim blandit eget. " \
       "Ut aliquet, odio ut feugiat bibendum, turpis leo feugiat nunc, non aliquet neque ipsum eu mi. Nullam lobortis fermentum dui. Nunc egestas sit amet ipsum quis congue." \
       " Aliquam eu molestie velit. Nunc ornare imperdiet felis, ut tempus eros vulputate vitae. Integer tristique mi vehicula, consectetur risus vel, elementum arcu."

blogs = [
	{"owner" : "john_test", "trip":"Trip to New Zealand", "title":"Day 1", "date":"2018-02-24", "content":"I have arrived in New Zealand, this place is pretty cool so far."},
	{"owner" : "john_test", "trip":"Trip to New Zealand", "title":"Day 2", "date":"2018-02-25", "content":"I ate some mountain oysters."},
	{"owner" : "bob_test", "trip":"Exploring the East", "title":"Chinaaaa", "date":"2017-04-25", "content":"What an amazing trip that was. Lovely!"},
	{"owner" : "cicero_test", "trip":"My Exile", "title":"Leges Clodiae", "date":"2017-12-11", "content":lorem},
	{"owner" : "brutus_test", "trip":"Papa don't Preach", "title":"Middle of March", "date":"2017-03-15", "content":"I am going to stab by stepfather today, excited!!"},
	{"owner" : "julius_test", "trip":"Checking out Alesia", "title":"Siege Time", "date":"2017-09-02", "content":"Setting up a siege around Alesia."},
	{"owner" : "julius_test", "trip":"Checking out Alesia", "title":"Fortception", "date":"2017-09-02", "content":"We built a fort around the fort."},
	{"owner" : "julius_test", "trip":"Checking out Alesia", "title":"Aftermath", "date":"2017-09-30", "content":"Cracking open a Gaul one with the boys."},
]

ratings  = [
	{"rater":"tarzan_test", "tripowner" : "john_test", "triptitle": "Trip to New Zealand", "score":"5"},
	{"rater":"alex_test", "tripowner" : "john_test", "triptitle": "Trip to New Zealand", "score":"3"},
	{"rater":"brutus_test", "tripowner" : "cicero_test", "triptitle": "My Exile", "score":"3"},
	{"rater":"julius_test", "tripowner" : "cicero_test", "triptitle": "My Exile", "score":"2"},
	{"rater":"julius_test", "tripowner" : "brutus_test", "triptitle": "Papa don't Preach", "score":"1"},
	{"rater":"vercingetorix", "tripowner" : "julius_test", "triptitle": "Checking out Alesia", "score":"1"},
	{"rater":"brutus_test", "tripowner" : "julius_test", "triptitle": "Checking out Alesia", "score":"5"},
]

comments = [
	{"rater":"tarzan_test", "postowner" : "john_test", "posttitle": "Day 1", "content":"Nice blog post!"},
	{"rater":"alex_test", "postowner" : "john_test", "posttitle": "Day 2", "content":"How did they taste?"},
	{"rater":"brutus_test", "postowner" : "cicero_test", "posttitle": "Leges Clodiae", "content":"FAKE NEWS!"},
	{"rater":"julius_test", "postowner" : "cicero_test", "posttitle": "Leges Clodiae", "content":"Allia iacta es"},
	{"rater":"julius_test", "postowner" : "brutus_test", "posttitle": "Middle of March", "content":"Et tu, Brute?"},
	{"rater":"vercingetorix", "postowner" : "julius_test", "posttitle": "Siege Time", "content":"Plz leave."},
	{"rater":"vercingetorix", "postowner" : "julius_test", "posttitle": "Fortception", "content":"Plz leave."},
	{"rater":"vercingetorix", "postowner" : "julius_test", "posttitle": "Aftermath", "content":"Not cool, bro."},
]

def populate():
	with open('countries.csv') as csvfile:
		line = 1
		countries = csv.reader(csvfile, delimiter=';', quotechar='|')
		print("Adding Destinations: ")
		for row in countries:
			print(str(line)+ ".)" + ', '.join(row))
			line = line +1
			cc = row[0]
			name = row[1]
			latitude = float(row[2])
			longitude = float(row[3])
			picPath = "flags\\" + row[4]
			add_destination(cc, name, latitude, longitude,picPath)

		for key, value in users.items():
			print("Creating user: " + key)
			add_user(username=key,hc=value)

		for trip in trips:
			print("Adding trip: " + trip["title"])
			add_trip(trip)

		for post in blogs:
			print("Adding blog post " + post["title"] + " to trip: " + post["trip"])
			add_post(post)

		for rating in ratings:
			print("Rating " + rating["triptitle"])
			add_rating(rating)

		for comment in comments:
			print("Adding comment to blog post " + comment["posttitle"])
			add_comment(comment)
            

def add_destination(cc, nam, lat, longi, path):
    d = Destination.objects.get_or_create(name=nam, latitude=lat, longitude=longi)[0]
    d.name=nam
    d.longitude=longi
    d.latitude=lat
    d.countryCode = cc
    d.flag = ImageFile(open(path, "rb"))
    d.save()
    return d

def add_user(username, hc):
	u = User.objects.get_or_create(username=username, password="test1234", email=username+"@test.com")[0]
	u.username = username
	u.password = "test1234"
	u.email = username + "@test.com"
	u.save()
	d = Destination.objects.get(name=hc)
	p = True
	if(username[0] == "b"):
		p = False
	profile = UserProfile.objects.get_or_create(user=u, homeCountry=d)[0]
	profile.user = u
	profile.public = p
	profile.homeCountry = d
	profile.save()

def add_trip(trip):
	sdate = datetime.strptime(trip["sdate"], "%Y-%m-%d").date()
	edate = datetime.strptime(trip["edate"], "%Y-%m-%d").date()
	u = User.objects.get(username__exact=trip['owner'])
	d = Destination.objects.get(name=trip['destination'])
	t = Trip.objects.get_or_create(owner=u, destination=d, startDate=sdate, endDate=edate)[0]
	t.owner = u
	t.destination = d
	t.title = trip["title"]
	t.startDate = sdate
	t.endDate = edate
	t.save()

def add_post(post):
	date = datetime.strptime(post["date"], "%Y-%m-%d").date()
	u = User.objects.get(username__exact=post['owner'])
	t = Trip.objects.get(owner=u, title=post["trip"])
	p = BlogPost.objects.get_or_create(user=u, trip=t, Date=date, title=post['title'])[0]
	p.user = u
	p.trip = t
	p.Date = date
	p.title = post["title"]
	p.content = post["content"]
	p.save()

def add_rating(rating):
	owner = User.objects.get(username__exact=rating['tripowner'])
	rater = User.objects.get(username__exact=rating['rater'])
	trip = Trip.objects.get(owner=owner, title=rating["triptitle"])
	s = ""
	try:
		Rating.objects.get(owner=rater, trip=trip)
		s = "Rating already exists"
	except Rating.DoesNotExist:
		r = Rating(owner=rater, trip=trip, score=int(rating['score']))
		r.save()
		s = "Rating created"
	print(s)

def add_comment(comment):
	owner = User.objects.get(username__exact=comment['postowner'])
	rater = User.objects.get(username__exact=comment['rater'])
	post = BlogPost.objects.get(user=owner, title=comment['posttitle'])
	c = Comment.objects.get_or_create(user=rater, post=post)[0]
	c.user = rater
	c.post = post
	c.content= comment['content']
	c.save()

# Start execution here!
if __name__ == '__main__':
	print("Auto-migrations")
	auto_migrations()
	print("Clearing media/flags")
	clear_media()
	print("Starting population script...")
	populate()
