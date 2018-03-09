import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                        'travelmate.settings')

import django
django.setup()
import random
import csv
from app.models import Destination

def populate():
    with open('countries.csv') as csvfile:
        countries = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in countries:
            print(', '.join(row))
            name = row[1]
            latitude = float(row[2])
            longitude = float(row[3])
            add_destination(name, latitude, longitude)
            

def add_destination(nam, lat, longi):
    d = Destination.objects.get_or_create(name=nam, latitude=lat, longitude=longi)[0]
    d.name=nam
    d.longitude=longi
    d.latitude=lat
    d.save()
    return d

# Start execution here!
if __name__ == '__main__':
    print("Starting Travelmate population script...")
    populate()
