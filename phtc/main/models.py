from django.db import models
from django.contrib.auth.models import User
from registration.signals import user_registered
from forms import UserRegistrationForm
from django_statsd.clients import statsd
from pagetree.models import Section
from django import forms


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
    data.disadvantaged = form.data["disadvantaged"]
    data.employment_location = form.data["employment_location"]
    data.position = form.data["position"]
    data.save()
    statsd.incr('user_registered')

user_registered.connect(user_created)


class DashboardInfo(models.Model):
    dashboard = models.OneToOneField(Section)
    info = models.TextField()

    def edit_form(self):
        class EditSectionForm(forms.Form):
            dashboard_info = forms.CharField(widget=forms.Textarea,
                                             initial=self.info)
        return EditSectionForm()
