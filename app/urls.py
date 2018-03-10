from django.conf.urls import url
from app import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^about/$', views.about, name='about'),
    url(r'^contact/$', views.contact, name='contact'),
    url(r'^pop_trips/$', views.pop_trips, name='pop_trips'),
    url(r'^recent_trips/$', views.recent_trips, name='recent_trips'),
    url(r'^welltrav_travellers/$', views.welltrav_travellers, name='welltrav_travellers'),
    url(r'^most_active_travellers/$', views.contact, name='most_active_travellers'),
    url(r'^passport/$', views.passport, name='passport'),
    url(r'^view_profile/$', views.view_profile, name='view_profile'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^add_trip/$', views.add_trip, name='add_trip'),
    url(r'^settings/$', views.settings, name='settings'),
    url(r'^my_trips/$', views.my_trips, name='my_trips')
]
