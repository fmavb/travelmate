"""travelmate URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from app import views as app_views
from django.contrib.auth import views as auth_views
from registration.backends.simple.views import RegistrationView
from . import settings
from django.views.static import serve


class MyRegistrationView(RegistrationView):
    def get_success_url(self, user):
        return '/app/settings/'


urlpatterns = [
                  url(r'^$', app_views.home, name='home'),
                  url(r'^admin/', admin.site.urls),
                  url(r'^login/$', auth_views.login, name='login'),
                  url(r'^logout/$', auth_views.logout, name='logout'),
                  url(r'^oauth/', include('social_django.urls', namespace='social')),
                  url(r'^accounts/register/$', MyRegistrationView.as_view(), name='registration_register'),
                  url(r'^accounts/', include('registration.backends.simple.urls')),

                  url(r'^app/', include('app.urls')),
                  url(r'^collectstatic/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
                  url(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
                  url(r'^(?P<username>[\w\-]+)/$', app_views.view_profile, name='view_profile'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

LOGIN_URL = '/login'
LOGOUT_URL = '/logout'
LOGIN_REDIRECT_URL = '/home'
