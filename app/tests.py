# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from populate_script import *
from django.core.urlresolvers import reverse
from app.models import *
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

def new_user(self):
    self.user = User.objects.create_user(username='testuser', password='12345')
    self.client.login(username='testuser', password='12345')
    user = UserProfile(user=User.objects.get(username='testuser'),
                       homeCountry=Destination.objects.get(name__exact="United Kingdom"))
    user.save()

def add_trip():
    trip = Trip(startDate="2018-03-08", endDate="2018-03-07",
                destination=Destination.objects.get(name__exact="United Kingdom"),
                owner=User.objects.get(username='testuser'))
    trip.save()


# Create your tests here.
class TestTripsModel(TestCase):
    def setUp(self):
        populate()
        new_user(self)

    def test_if_startDate_after_endDate(self):
        add_trip()
        self.assertRaises(ValidationError)
        #self.assertEqual((trip.startDate <= trip.endDate), True)
    


class TestTripsView(TestCase):

    def setUp(self):
        populate()
        new_user(self)

    def test_if_correct_view_when_no_trips(self):
        response = self.client.get(reverse('my_trips'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "You have not added any trips yet, what are you waiting for?")
        self.assertQuerysetEqual(response.context['trips'], [])

    def test_if_correct_view_when_trips_present(self):
        response = self.client.get(reverse('my_trips'))
        add_trip()
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'United Kingdom')

    def breakDown(self):
        self.client.logout()

class TestHomeView(TestCase):

    def setUp(self):
        populate()
        new_user(self)

    def test_if_text_displayed_correctly_when_user_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response,"Welcome to Travelmate!")

    def test_if_text_displayed_correctly_when_user_is_logged_in(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code,200)
        self.assertContains(response, "Welcome to Travelmate, testuser!")

    def breakDown(self):
        self.client.logout()

class TestSettingsView(TestCase):

    def setUp(self):
        populate()
        new_user(self)

    def test_if_home_country_is_displayed(self):
        response = self.client.get(reverse('settings'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'United Kingdom')

    def test_if_redirected_if_user_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse('passport'))
        self.assertRedirects(response, '/accounts/login/?next=/app/settings/')

    def breakDown(self):
        self.client.logout()

class TestAboutView(TestCase):

    def setUp(self):
        populate()
        new_user(self)

    def test_if_about_page_loads_when_logged_in(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)

    def test_if_about_page_loads_when_logged_out(self):
        self.client.logout()
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)

    def breakDown(self):
        self.client.logout()

class TestPassportView(TestCase):

    def setUp(self):
        populate()
        new_user(self)

    def test_if_country_is_shown(self):
        response = self.client.get(reverse('passport'))
        self.assertEqual(response.status_code,200)
        self.assertContains(response, 'United Kingdom')

    def test_if_redirected_if_user_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse('passport'))
        self.assertRedirects(response, '/accounts/login/?next=/app/passport/')