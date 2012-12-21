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
    umc = models.TextField(default='')
    employment_location = models.TextField()
    other_employment_location = models.TextField()
    position = models.TextField()
    other_position_category = models.TextField()
    dept_health = models.TextField()
    geo_dept_health = models.TextField()
    experience = models.TextField()
    rural = models.TextField()
    degree = models.TextField()
    disadvantaged = models.TextField()

    #NYNJ additions
    is_nylearns = models.BooleanField(default=False)
    nylearns_course_init = models.TextField(default='none')
    nylearns_user_id = models.TextField(default='none')


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
    data.umc = form.data["umc"]
    data.employment_location = form.data["employment_location"]
    data.position = form.data["position"]
    data.dept_health = form.data["dept_health"]
    data.geo_dept_health = form.data["geo_dept_health"]
    data.experience = form.data["experience"]
    data.rural = form.data["rural"]
    data.degree = form.data["degree"]

    # NYNJ additions
    data.is_nylearns = form.data["is_nylearns"] 
    data.nylearns_username = form.data["nylearns_username"]
    data.nylearns_course_init = form.data["nylearns_course_init"]
    data.nylearns_user_id = form.data["nylearns_user_id"]

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

class NYLEARNS_Course_Map(models.Model):
    id = models.AutoField(primary_key=True)
    courseID = models.TextField()
    phtc_url = models.TextField()

    def __unicode__(self):
        return "url path:%s" % self.phtc_url
