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


def migration():
    trips = Trip.objects.all()
    for trip in trips:
        owner = trip.owner
        ownerProfile = UserProfile.objects.get(user=owner)
        trip.origin = ownerProfile.homeCountry
        trip.save()


if __name__ == '__main__':
    print("Running migration script")
    migration()
