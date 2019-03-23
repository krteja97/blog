from django.db import models

# Create your models here.
class User(models.Model):
	name = models.CharField(max_length=50)
	user_name = models.CharField(max_length=20)
	password = models.CharField(max_length=30)
	city = models.CharField(max_length=20)
	dob = models.DateField('Birthday');

	def __str__(self):
		return self.user_name;

class Tweet(models.Model):
	author = models.ForeignKey(User,on_delete = models.CASCADE);
	heading = models.CharField(max_length = 30);
	tweettext = models.CharField(max_length = 200);
	publish_date = models.DateTimeField();

	def __str__(self):
		return self.heading;
