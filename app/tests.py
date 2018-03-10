# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from populate_script import *
from django.core.urlresolvers import reverse
from app.models import *
from django.contrib.auth.models import User


# Create your tests here.
class TestTripsModel(TestCase):
    def setUp(self):
        populate()
        self.user = User.objects.create_user(username='testuser', password='12345')
        login = self.client.login(username='testuser', password='12345')
        user = UserProfile(user=User.objects.get(username='testuser'),
                           homeCountry=Destination.objects.get(name__exact="United Kingdom"))
        user.save()

    def test_if_startDate_after_endDate(self):
        trip = Trip(startDate="2018-03-08", endDate="2018-03-07",
                    destination=Destination.objects.get(name__exact="United Kingdom"),
                    owner=User.objects.get(username='testuser'))
        trip.save()
        self.assertEqual((trip.startDate <= trip.endDate), True)

    


class TestTripsView(TestCase):

    def setUp(self):
        populate()
        self.user = User.objects.create_user(username='testuser', password='12345')
        login = self.client.login(username='testuser', password='12345')
        user = UserProfile(user=User.objects.get(username='testuser'),
                           homeCountry=Destination.objects.get(name__exact="United Kingdom"))
        user.save()

    def test_if_correct_view_when_no_trips(self):
        response = self.client.get(reverse('trips'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "You have not added any trips yet, what are you waiting for?")
        self.assertQuerysetEqual(response.context['trips'], [])

