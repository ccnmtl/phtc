from django.db import models
from django.contrib.auth.models import User
from registration.signals import user_registered
from forms import UserRegistrationForm
from django_statsd.clients import statsd
from pagetree.models import Section
from django import forms


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    fname = models.TextField()
    lname = models.TextField()
    work_city = models.TextField()
    work_state = models.TextField()
    work_zip = models.TextField()
    sex = models.TextField()
    age = models.TextField()
    origin = models.TextField()
    ethnicity = models.TextField()
    disadvantaged = models.TextField()
    employment_location = models.TextField()
    other_employment_location = models.TextField()
    position = models.TextField()
    other_position_category = models.TextField()
    dept_health = models.TextField()
    geo_dept_health = models.TextField()
    experience = models.TextField()
    rural = models.TextField()
    degree = models.TextField()

    def __str__(self):
        return "%s's profile" % self.user


def user_created(sender, user, request, **kwargs):
    form = UserRegistrationForm(request.POST)
    data = UserProfile(user=user)
    data.fname = form.data["fname"]
    data.lname = form.data["lname"]
    data.work_city = form.data["work_city"]
    data.work_state = form.data["work_state"]
    data.work_zip = form.data["work_zip"]
    data.sex = form.data["sex"]
    data.age = form.data["age"]
    data.origin = form.data["origin"]
    data.ethnicity = form.data["ethnicity"]
    data.employment_location = form.data["employment_location"]
    data.position = form.data["position"]
    data.dept_health = form.data["dept_health"]
    data.geo_dept_health = form.data["geo_dept_health"]
    data.experience = form.data["experience"]
    data.rural = form.data["rural"]
    data.degree = form.data["degree"]

    try:
        data.other_position_category = form.data["other_position_category"]
    except:
        pass

    try:
        data.other_employment_location = form.data["other_location"]
    except:
        pass

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
