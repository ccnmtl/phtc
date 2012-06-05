from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

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
    
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            profile = UserProfile()
            profile.user = instance
            
    post_save.connect(create_user_profile, sender = User)
