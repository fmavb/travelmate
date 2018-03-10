# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from app.models import Destination, UserProfile, Rating, Trip, BlogPost, Comment, PostImage

# Register your models here.
admin.site.register(Destination)
admin.site.register(UserProfile)
admin.site.register(Rating)
admin.site.register(Trip)
admin.site.register(BlogPost)
admin.site.register(Comment)
admin.site.register(PostImage)