from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

# Create your models here.
class Destination(models.Model):
	name = models.CharField(max_length=85)
	longitude = models.FloatField()
	latitude = models.FloatField()
	
	def __str__(self): # For Python 2, use __unicode__ too
		return self.name


class UserProfile(models.Model):
	user = models.OneToOneField(User)
	profileID = models.AutoField(primary_key=True)
	profilePic = models.ImageField(upload_to='profile_images', blank=True)
	homeCountry = models.ForeignKey(Destination,on_delete=models.CASCADE)
	public = models.BooleanField(default=False)
	
	def __str__(self):
		return self.user.username
		
	def as_dict(self):
		return {
			"lat": self.homeCountry.latitude,
			"lng": self.homeCountry.longitude,
		}


class Trip(models.Model):
	owner = models.ForeignKey(User,on_delete=models.CASCADE)
	tripID = models.AutoField(primary_key=True)
	startDate = models.DateField()
	endDate = models.DateField()
	public = models.BooleanField(default=False)
	destination = models.ForeignKey(Destination,on_delete=models.CASCADE)

	def __str__(self): # For Python 2, use __unicode__ too
		return self.owner.username + str(self.tripID)
		
		
	def as_dict(self):
		return {
			"lat": self.destination.latitude,
			"lng": self.destination.longitude,
			"name": self.destination.name,
		}

class Rating(models.Model):
	score = models.IntegerField()
	owner = models.ForeignKey(User, on_delete=models.CASCADE)
	trip = models.ForeignKey(Trip, related_name='ratings')

	def __str__(self):
		return str(self.score)

class BlogPost(models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	postID = models.AutoField(primary_key=True)
	Date = models.DateField()
	content = models.TextField()
	trip = models.ForeignKey(Trip, related_name='posts')

	def __str__(self):
		return self.content
		
class Comment(models.Model):
	commentID = models.AutoField(primary_key=True)
	Date = models.DateField()
	content = models.CharField(max_length=200)
	post = models.ForeignKey(BlogPost, related_name='comments')
	user = models.ForeignKey(User,on_delete=models.CASCADE)

	def __str__(self):
		return self.content

		
class PostImage(models.Model):
	post = models.ForeignKey(BlogPost, related_name='images')
	image = models.ImageField()
