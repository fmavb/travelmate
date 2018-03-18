# -*- coding: utf-8 -*-
from django.test import TestCase
from populate_script import *
from django.core.urlresolvers import reverse
from app.models import *
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone


def new_user(self):
    self.user = User.objects.create_user(username='testuser', password='12345')
    self.client.login(username='testuser', password='12345')
    user = UserProfile(user=User.objects.get(username='testuser'),
                       homeCountry=Destination.objects.get(name__exact="United Kingdom"))
    user.save()


def add_trip():
    trip = Trip(startDate="2018-03-08", endDate="2018-03-07",
                destination=Destination.objects.get(name__exact="United Kingdom"),
                owner=User.objects.get(username='testuser'), title='UK'
                )
    trip.save()


def add_blog():
    blog = BlogPost(user=User.objects.get(username="testuser"), trip=Trip.objects.get(title='UK'), title="Post",
                    content="Some content", Date=timezone.now())
    blog.save()

def add_comment():
    comment = Comment(user=User.objects.get(username='testuser'),post=BlogPost.objects.get(title="Post"),content="A comment")
    comment.save()


# Create your tests here.
class TestTripsModel(TestCase):
    def setUp(self):
        populate()
        new_user(self)

    def test_if_startDate_after_endDate(self):
        add_trip()
        self.assertRaises(ValidationError)
        # self.assertEqual((trip.startDate <= trip.endDate), True)


class TestMyProfileView(TestCase):

    def setUp(self):
        populate()
        new_user(self)

    def test_if_correct_view_when_no_trips(self):
        response = self.client.get(reverse('view_profile', kwargs={'username': 'testuser'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "The user has no trips yet!")
        self.assertQuerysetEqual(response.context['elems'], [])

    def test_if_correct_view_when_trips_present(self):
        add_trip()
        response = self.client.get(reverse('view_profile', kwargs={'username': 'testuser'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "United Kingdom")

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
        self.assertContains(response, "Welcome to Travelmate!")

    def test_if_text_displayed_correctly_when_user_is_logged_in(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
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
        self.assertRedirects(response, '/login/?next=/app/settings/')

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
        add_trip()
        response = self.client.get(reverse('passport'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'United Kingdom')

    def test_if_redirected_if_user_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse('passport'))
        self.assertRedirects(response, '/login/?next=/app/passport/')

    def test_if_no_countries(self):
        response = self.client.get(reverse('passport'))
        self.assertContains(response, "You haven't added any trips yet.")

    def breakDown(self):
        self.client.logout()


class TestTripView(TestCase):
    def setUp(self):
        populate()
        new_user(self)

    def test_if_trip_view_works(self):
        add_trip()
        trip = Trip.objects.get(title='UK')
        slug = trip.slug
        response = self.client.get(reverse('view_trip', kwargs={'username': 'testuser', 'trip_name_slug': slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'United Kingdom')
        self.assertContains(response, 'UK')

    def breakDown(self):
        self.client.logout()


class TestBlogView(TestCase):
    def setUp(self):
        populate()
        new_user(self)

    def test_if_blog_view_works_if_no_comment(self):
        add_trip()
        add_blog()
        blog = BlogPost.objects.get(title='Post')
        blogSlug = blog.slug
        trip = Trip.objects.get(title='UK')
        tripSlug = trip.slug
        response = self.client.get(reverse('blog_post', kwargs={'username': 'testuser', 'trip_name_slug': tripSlug,
                                                                'post_name_slug': blogSlug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Post')
        self.assertContains(response, 'Some content')
        self.assertContains(response,'No comments')

    def test_if_blog_view_shows_comments(self):
        add_trip()
        add_blog()
        add_comment()
        blog = BlogPost.objects.get(title='Post')
        blogSlug = blog.slug
        trip = Trip.objects.get(title='UK')
        tripSlug = trip.slug
        response = self.client.get(reverse('blog_post', kwargs={'username': 'testuser', 'trip_name_slug': tripSlug,
                                                                'post_name_slug': blogSlug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Post')
        self.assertContains(response, 'Some content')
        self.assertContains(response, 'A comment')

    def breakDown(self):
        self.client.logout()
