import os, shutil

from django.core.files.images import ImageFile

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                        'travelmate.settings')

import django
django.setup()
import random
import csv
from app.models import Destination

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

def populate():
	with open('countries.csv') as csvfile:
		line = 1
		countries = csv.reader(csvfile, delimiter=';', quotechar='|')
		for row in countries:
			print(str(line)+ ".)" + ', '.join(row))
			line = line +1
			cc = row[0]
			name = row[1]
			latitude = float(row[2])
			longitude = float(row[3])
			picPath = "flags\\" + row[4]
			add_destination(cc, name, latitude, longitude,picPath)
            

def add_destination(cc, nam, lat, longi, path):
    d = Destination.objects.get_or_create(name=nam, latitude=lat, longitude=longi)[0]
    d.name=nam
    d.longitude=longi
    d.latitude=lat
    d.countryCode = cc
    d.flag = ImageFile(open(path, "rb"))
    d.save()
    return d

# Start execution here!
if __name__ == '__main__':
	print("Clearing media/flags")
	clear_media()
	print("Starting Country population script...")
	populate()
