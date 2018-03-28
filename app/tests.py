# -*- coding: utf-8 -*-
from django.test import TestCase
from populate_script import *
from django.core.urlresolvers import reverse
from app.models import *
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
import operator

# In setUp, database is populated using the population_script. Also, a user is created where it is relevant
# In breakDown, the user that is logged in is logged out.

## Helper function

# Creates a new user 'testuser'
def new_user(self):
    self.user = User.objects.create_user(username='testuser', password='12345')
    self.client.login(username='testuser', password='12345')
    user = UserProfile(user=User.objects.get(username='testuser'),
                       homeCountry=Destination.objects.get(name__exact="United Kingdom"))
    user.save()

# Adds a new trip with owner 'testuser'
def add_trip():
    trip = Trip(startDate="2018-03-05", endDate="2018-03-07",
                destination=Destination.objects.get(name__exact="United Kingdom"),
                owner=User.objects.get(username='testuser'), title='UK'
                )
    trip.save()

# Adds a new blog post related to 'testuser''s trip
def add_blog():
    blog = BlogPost(user=User.objects.get(username="testuser"), trip=Trip.objects.get(title='UK'), title="Post",
                    content="Some content", Date=timezone.now())
    blog.save()


# Adds a comment to the blogpost cited above
def add_comment():
    comment = Comment(user=User.objects.get(username='testuser'), post=BlogPost.objects.get(title="Post"),
                      content="A comment")
    comment.save()

# Returns a sorted dictionary with values in descending order
def sort_dict(d):
    user_list = []
    for key, value in sorted(d.items(), key=operator.itemgetter(1), reverse=True):
        user_list.append([key, value])
    return user_list


# Create your tests here.
class TestTripsModel(TestCase):
    def setUp(self):
        populate()
        new_user(self)

    def test_if_startDate_after_endDate(self):
        trip = Trip(startDate="2018-03-08", endDate="2018-03-07",
                    destination=Destination.objects.get(name__exact="United Kingdom"),
                    owner=User.objects.get(username='testuser'), title='UK'
                    )
        trip.save()
        self.assertRaises(ValidationError)
        # self.assertEqual((trip.startDate <= trip.endDate), True)

        def breakDown(self):
            self.client.logout()


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

    def test_if_user_redirect_when_UserProfile_does_not_exist(self):
        self.user = User.objects.create_user(username='testuser1', password='12345')
        self.client.login(username='testuser1', password='12345')

        response = self.client.get(reverse('home'))

        self.assertRedirects(response, reverse('settings'))

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

    def test_blog_view_redirect_when_logged_out_and_user_private(self):
        add_trip()
        user = User.objects.get(username='testuser')
        user = UserProfile.objects.get(user=user)
        user.public = False
        user.save()
        self.client.logout()
        trip = Trip.objects.get(title='UK')
        tripSlug = trip.slug
        response = self.client.get(reverse('view_trip', kwargs={'username': 'testuser', 'trip_name_slug': tripSlug}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/')

    def test_blog_view_when_logged_out_and_user_public(self):
        add_trip()
        add_blog()
        user = User.objects.get(username='testuser')
        user = UserProfile.objects.get(user=user)
        user.public = True
        user.save()
        self.client.logout()
        trip = Trip.objects.get(title='UK')
        tripSlug = trip.slug
        response = self.client.get(reverse('view_trip', kwargs={'username': 'testuser', 'trip_name_slug': tripSlug}))
        self.assertEqual(response.status_code, 200)
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
        self.assertContains(response, 'No comments')

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

    def test_blog_view_redirect_when_logged_out_and_user_private(self):
        add_trip()
        add_blog()
        user = User.objects.get(username='testuser')
        user = UserProfile.objects.get(user=user)
        user.public = False
        user.save()
        self.client.logout()
        blog = BlogPost.objects.get(title='Post')
        blogSlug = blog.slug
        trip = Trip.objects.get(title='UK')
        tripSlug = trip.slug
        response = self.client.get(reverse('blog_post', kwargs={'username': 'testuser', 'trip_name_slug': tripSlug,
                                                                'post_name_slug': blogSlug}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/')

    def test_blog_view_redirect_when_logged_out_and_user_public(self):
        add_trip()
        add_blog()
        user = User.objects.get(username='testuser')
        user = UserProfile.objects.get(user=user)
        user.public = True
        user.save()
        self.client.logout()
        blog = BlogPost.objects.get(title='Post')
        blogSlug = blog.slug
        trip = Trip.objects.get(title='UK')
        tripSlug = trip.slug
        response = self.client.get(reverse('blog_post', kwargs={'username': 'testuser', 'trip_name_slug': tripSlug,
                                                                'post_name_slug': blogSlug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Post')

    def breakDown(self):
        self.client.logout()

class TestPopularTripsView(TestCase):
    def setUp(self):
        populate()

    def test_if_trips_are_shown_in_popular_order(self):
        popTrips = Trip.objects.order_by('score').reverse()[:10]
        response = self.client.get(reverse('pop_trips'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['elems'], [repr(elt) for elt in popTrips])

    def breakDown(self):
        self.client.logout()

class TestRecentTripsView(TestCase):
    def setUp(self):
        populate()

    def test_if_trips_are_shown_in_most_recent_order(self):
        recentTrips = Trip.objects.order_by('startDate').reverse()[:10]
        response = self.client.get(reverse('recent_trips'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['elems'], [repr(elt) for elt in recentTrips])

    def breakDown(self):
        self.client.logout()

class TestMostActiveTravellersView(TestCase):
    def setUp(self):
        populate()

    def test_if_travellers_shown_by_number_of_blogposts(self):
        users = {}
        posts = BlogPost.objects.all()
        for post in posts:
            users[post.user] = users.get(post.user, 0) + 1

        sorted = sort_dict(users)[:10]

        response = self.client.get(reverse('most_active_travellers'))

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['elems'], [repr(elt) for elt in sorted])

    def breakDown(self):
        self.client.logout()

class TestWellTravelledView(TestCase):
    def setUp(self):
        populate()

    def test_if_users_shown_by_number_of_trips(self):
        users = {}
        trips = Trip.objects.all()

        for trip in trips:
            users[trip.owner] = users.get(trip.owner, 0) + 1

        sorted = sort_dict(users)[:10]

        response = self.client.get(reverse('best_travelled'))

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['elems'], [repr(elt) for elt in sorted])

    def breakDown(self):
        self.client.logout()

class TestSearchView(TestCase):
    def setUp(self):
        populate()

    def test_if_search_works(self):
        users = UserProfile.objects.filter(user__username__icontains='julius')[:10]

        url = reverse('search') + "?search-bar=julius"
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['login_required'], [repr(elt) for elt in users])

    def breakDown(self):
        self.client.logout()
