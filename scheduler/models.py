########################################################################################
#  REFERENCES
#
#  Title: How to Extend Django User Model
#  Author: Vitor Freitas
#  Date: 7/22/2016
#  URL: https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html#onetoone
#
#  Title: django-multiselectfield
#  Author: blag, Goin, tomasgarzon
#  Date: 2/20/2020
#  Code version: 0.1.12
#  URL: https://pypi.org/project/django-multiselectfield/
#  Software License: LGPL v3
#
#  Title: How to Create a To-do List App Using Django
#  Author: Ashwin Joy
#  URL: https://pythonistaplanet.com/to-do-list-app-using-django/
#
#  Title: cal/models.py
#  Author: Hui Wen
#  Date: 7/24/2018
#  URL: https://www.huiwenteo.com/normal/2018/07/24/django-calendar.html
#
#  Title: cal/models.py
#  Author: Hui Wen
#  Date: 7/29/2018
#  URL: https://www.huiwenteo.com/normal/2018/07/29/django-calendar-ii.html
#
#  Title: chat/models.py
#  Author: Kevin Ndung'u
#  Date: 5/15/2018
#  URL: https://www.twilio.com/blog/2018/05/build-chat-python-django-applications-programmable-chat.html
########################################################################################


from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from multiselectfield import MultiSelectField
import datetime



# Create your models here.

# Profile model, an extension of the built-in Django user model
# Used to keep track of additional information about the user
class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name = "profile", null=True)

	# To retrieve the list of classes the user is enrolled in, call self.studentclass_set.all()

	def __str__(self):
		return self.user.username

# Signal function that automatically creates a corresponding instance of a Profile model whenever an instance of a User model is created
# Reference: How to extend Django User Model, Vitor Freitas
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user = instance)

# Signal function that automatically creates a corresponding instance of a Profile model whenever an instance of a User model is created
# Reference: How to extend Django User Model by Vitor Freitas
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
	instance.profile.save()

# NoteFile, a model for storing notes a user has uploaded for their classes
class NoteFile(models.Model):
	note = models.FileField()
	title = models.CharField(max_length=200, default='')
	upload_time = models.DateTimeField(auto_now=True)
	user = models.ManyToManyField(Profile)

	def __str__(self):
		return self.title


# StudentClass model, a model that contains information about courses users are enrolled in
# Reference: django-multiselectfield by blag et al.
class StudentClass(models.Model):
	class_name = models.CharField(max_length=200, default='')
	instructor = models.CharField(max_length=200, default='')
	users = models.ManyToManyField(Profile)
	start_time = models.TimeField(null=True)
	end_time = models.TimeField(null=True)
	location = models.CharField(max_length=200, default='')
	enrolled_users_count = models.IntegerField(default=0)
	notes = models.ManyToManyField(NoteFile)
	DAY_OF_THE_WEEK = (
		("Sunday", "Sunday"),
		("Monday", "Monday"),
		("Tuesday", "Tuesday"),
		("Wednesday", "Wednesday"),
		("Thursday", "Thursday"),
		("Friday", "Friday"),
		("Saturday", "Saturday"),
	)

	days_of_the_week = MultiSelectField(choices = DAY_OF_THE_WEEK)


	class Meta:
		verbose_name_plural = 'Student Classes'
		unique_together = [['class_name', 'instructor']]

	def __str__(self):
		return self.class_name


# TodoListItem model, a model representing a single task on a todolist
# Reference: How to Create a To-do List App Using Django by Ashwin Joy
class TodoListItem(models.Model):
    content = models.TextField()
    users = models.ManyToManyField(Profile)

    def __str__(self):
    	return self.content

# Event model, a model containing information about events the user has scheduled
# Reference: cals/views.py by Hui Wen
class Event(models.Model):
	title = models.CharField(max_length=200)
	description = models.TextField()
	start_time = models.DateTimeField()
	users = models.ManyToManyField(Profile)

	@property
	def get_html_url(self):
		url = reverse('event_edit', args=(self.id,))
		return f'<a href="{url}"> {self.title} </a>'

	def __str__(self):
		return self.title

# Room model, a model for storing details about each chat room
# Reference: chat/views.py by Kevin Ndung'u
class Room(models.Model):
    """Represents chat rooms that users can join"""
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=100)
    slug = models.CharField(max_length=50)

    def __str__(self):
        """Returns human-readable representation of the model instance."""
        return self.name
