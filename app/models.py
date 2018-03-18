from django.db import models
from django.core.exceptions import ValidationError
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User


# Create your models here.
class Destination(models.Model):
    name = models.CharField(max_length=85)
    longitude = models.FloatField()
    latitude = models.FloatField()
    countryCode = models.CharField(max_length=5)
    flag = models.ImageField(blank=True)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    profileID = models.AutoField(primary_key=True)
    profilePic = models.ImageField(upload_to='profile_images', blank=True, default='profile_images/default.jpg')
    homeCountry = models.ForeignKey(Destination, on_delete=models.CASCADE)
    public = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    # Returns homeCountry location attributes of a UserProfile object as a dictionary
    def as_dict(self):
        return {
            "lat": self.homeCountry.latitude,
            "lng": self.homeCountry.longitude,
        }

    def get_home_name(self):
        return self.homeCountry.name


class Trip(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    tripID = models.AutoField(primary_key=True)
    startDate = models.DateField()
    endDate = models.DateField()
    public = models.BooleanField(default=False)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE)
    title = models.CharField(max_length=85)
    slug = models.SlugField(unique=True)
    score = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title) + "-" + str(self.owner.id)
        super(Trip, self).save(*args, **kwargs)

    def __str__(self):  # For Python 2, use __unicode__ too
        return self.slug

    # Returns the attributes of a Trip object as a dictionary
    def as_dict(self):
        return {
            "lat": self.destination.latitude,
            "lng": self.destination.longitude,
            "sDate": str(self.startDate),
            "eDate": str(self.endDate),
            "name": self.destination.name,
            'title': self.title,
            'slug': self.slug,
        }

    # Check if startDate is before or equal to endData
    def clean(self):
        if self.startDate > self.endDate:
            raise ValidationError('Start date is after end date')


class Rating(models.Model):
    score = models.IntegerField(default=0)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    trip = models.ForeignKey(Trip, related_name='ratings')

    def __str__(self):
        return self.owner.username + " - " + self.trip.title + " - " + str(self.score)


class BlogPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    postID = models.AutoField(primary_key=True)
    Date = models.DateField()
    content = models.TextField()
    trip = models.ForeignKey(Trip, related_name='posts')
    title = models.CharField(max_length=85)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title) + "-" + str(self.trip.tripID)
        super(BlogPost, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Comment(models.Model):
    commentID = models.AutoField(primary_key=True)
    Date = models.DateTimeField(auto_now_add=True)
    content = models.CharField(max_length=255)
    post = models.ForeignKey(BlogPost, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username + " - " + self.post.title

    def as_dict(self):
        return {
            "date": self.Date.date().__str__(),
            "content": self.content,
            "user": self.user.username,
        }


class PostImage(models.Model):
    post = models.ForeignKey(BlogPost, related_name='images')
    caption = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to='photos/')
    name = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.name = self.image.name
        super(PostImage, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
