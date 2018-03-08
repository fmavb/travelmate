from django.conf.urls import url
from app import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'about', views.about, name='about'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^add_trip/$', views.add_trip, name='add_trip'),
    url(r'^settings/$', views.settings, name='settings'),
    url(r'^trips/$', views.trips, name='trips')
]
