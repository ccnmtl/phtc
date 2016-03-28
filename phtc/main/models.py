from django.db import models
from django.contrib.auth.models import User
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

    # NYNJ additions
    is_nylearns = models.BooleanField(default=False)
    nylearns_course_init = models.TextField(default='none')
    nylearns_user_id = models.TextField(default='none')

    def __str__(self):
        return "%s's profile" % self.user


class DashboardInfo(models.Model):
    dashboard = models.OneToOneField(Section)
    info = models.TextField(default='')

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


class ModuleType(models.Model):
    module_type = models.OneToOneField(Section)
    info = models.TextField(default='')

    def edit_form(self):
        class EditModuleForm(forms.Form):
            module_type_form = forms.CharField(widget=forms.Textarea,
                                               initial=self.info,
                                               label='Module Type')
        return EditModuleForm()


class SectionCss(models.Model):
    section_css = models.OneToOneField(Section)
    css_field = models.TextField()

    def edit_form(self):
        class EditSectionCssForm(forms.Form):
            section_css_field = forms.CharField(widget=forms.Textarea,
                                                initial=self.css_field)
        return EditSectionCssForm()
