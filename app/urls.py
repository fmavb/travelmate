from django.conf.urls import url
from app import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^about/$', views.about, name='about'),
    url(r'^contact/$', views.contact, name='contact'),
    url(r'^terms-of-use/$', views.terms_of_use, name='terms_of_use'),
    url(r'^privacy-policy/$', views.privacy_policy, name='privacy_policy'),
    url(r'^results/$', views.search, name='search'),

    url(r'^pop_trips/$', views.pop_trips, name='pop_trips'),
    url(r'^recent_trips/$', views.recent_trips, name='recent_trips'),
    url(r'^best_travelled/$', views.best_travelled, name='best_travelled'),
    url(r'^most_active_travellers/$', views.most_active_travellers, name='most_active_travellers'),

    url(r'^passport/$', views.passport, name='passport'),
    url(r'^add_trip/$', views.add_trip, name='add_trip'),

    url(r'^settings/$', views.settings, name='settings'),
    url(r'^ajax/like_trip/$', views.like_trip, name='like_trip'),
    url(r'^ajax/comment/$', views.comment, name='comment'),
    url(r'^ajax/check_title/$', views.check_title, name='check_title'),
    url(r'^(?P<username>[\w\-]+)/$', views.view_profile, name='view_profile'),

    url(r'^(?P<username>[\w\-]+)/delete_trip/(?P<trip_name_slug>[\w\-]+)/$', views.delete_trip, name='delete_trip'),
    url(r'^(?P<username>[\w\-]+)/edit_trip/(?P<trip_name_slug>[\w\-]+)/$', views.edit_trip, name='edit_trip'),
    url(r'^(?P<username>[\w\-]+)/(?P<trip_name_slug>[\w\-]+)/$', views.view_trip, name='view_trip'),
    url(r'^(?P<username>[\w\-]+)/(?P<trip_name_slug>[\w\-]+)/add_blog_post/$', views.add_blog_post,
        name='add_blog_post'),

    url(r'^(?P<username>[\w\-]+)/(?P<trip_name_slug>[\w\-]+)/edit_post/(?P<post_name_slug>[\w\-]+)/$',
        views.edit_post, name='edit_post'),
    url(r'^(?P<username>[\w\-]+)/(?P<trip_name_slug>[\w\-]+)/delete_post/(?P<post_name_slug>[\w\-]+)/$',
        views.delete_post, name='delete_post'),
    url(r'^(?P<username>[\w\-]+)/(?P<trip_name_slug>[\w\-]+)/(?P<post_name_slug>[\w\-]+)/$', views.blog_post,
        name='blog_post'),
    url(r'^(?P<username>[\w\-]+)/(?P<trip_name_slug>[\w\-]+)/(?P<post_name_slug>[\w\-]+)/upload_images/$',
        views.upload_images, name='upload_images'),
    url(
        r'^(?P<username>[\w\-]+)/(?P<trip_name_slug>[\w\-]+)/(?P<post_name_slug>[\w\-]+)/delete_image/(?P<image_name>[\w\-.]+)/$',
        views.delete_image, name='delete_image'),
]
