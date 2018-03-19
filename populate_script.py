import os, shutil
from django.core.files.images import ImageFile
from django.core.management import execute_from_command_line

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                        'travelmate.settings')

import django
django.setup()
import random
import csv
from django.contrib.auth.models import User
from app.models import Destination, UserProfile

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
         "brutus_test":"Australia", "mike_test":"South Africa"}

trips = {
	"john_test" : {"title": "Trip to New Zealand", "destination":"New Zealand", "s"},
}

def populate():
	with open('countries.csv') as csvfile:
		line = 1
		# countries = csv.reader(csvfile, delimiter=';', quotechar='|')
		# for row in countries:
		# 	print(str(line)+ ".)" + ', '.join(row))
		# 	line = line +1
		# 	cc = row[0]
		# 	name = row[1]
		# 	latitude = float(row[2])
		# 	longitude = float(row[3])
		# 	picPath = "flags\\" + row[4]
		# 	add_destination(cc, name, latitude, longitude,picPath)

		for key, value in users.items():
			print("Creating user: " + key)
			add_user(username=key,hc=value)
            

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

# Start execution here!
if __name__ == '__main__':
	# print("Auto-migrations")
	# auto_migrations()
	# print("Clearing media/flags")
	# clear_media()
	print("Starting population script...")
	populate()
