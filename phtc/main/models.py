from django.db import models
from django.contrib.auth.models import User
from registration.signals import user_registered
from forms import UserRegistrationForm

# define your models here
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    sex = models.TextField()
    age = models.TextField()
    origin = models.TextField()
    ethnicity = models.TextField()
    disadvantaged = models.TextField()
    employment_location = models.TextField()
    position = models.TextField()
    
    def __str__(self):
        return "%s's profile" % self.user
    
def user_created(sender, user, request, **kwargs):
	form = UserRegistrationForm(request.POST)
	data = UserProfile(user=user)
        data.sex = form.data["sex"]
        data.age = form.data["age"]
        data.origin = form.data["origin"]
        data.ethnicity = form.data["ethnicity"]
        disadvantaged = form.data["disadvantaged"]
        employment_location = form.data["employment_location"]
        position = form.data["position"]
	data.save()

user_registered.connect(user_created)
