from django import forms
from registration.forms import RegistrationForm


attrs_dict = {'class': 'required'}


class UserRegistrationForm(RegistrationForm):
    sex = forms.CharField(
        max_length=6,
        label="What is your sex?",
        widget=forms.Select(choices=[('Please Select', 'Please Select'),
                                     ('male', 'Male'),
                                     ('female', 'Female')])
        )
    age = forms.CharField(
        label="What is your age?",
        widget=forms.Select(choices=[('Please Select', 'Please Select'),
                                     ('Under 20', 'Under 20 Years'),
                                     ('20-29', '20-29 Years'),
                                     ('30-39', '30-39 Years'),
                                     ('40-49', '40-49 Years'),
                                     ('50-59', '50-59 Years'),
                                     ('60-69', '60-69 Years'),
                                     ('70 or older', '70 Years or Older'),
                                     ('Prefer not to answer',
                                      'I prefer not to answer')])
        )
    origin = forms.CharField(
        label="Are you of Hispanic. Latino, or Spanish origin?",
        widget=forms.Select(choices=[('Please Select', 'Please Select'),
                                     ('yes', 'Yes'),
                                     ('no', 'No'),
                                     ('Prefer not to answer',
                                      'I prefer not to answer')])
        )
    ethnicity = forms.CharField(
        label="Which of these best represent your race/ethnicity?",
        widget=forms.Select(
            choices=[
                ('Please Select', 'Please Select'),
                ('American Indian or Alaskan Native',
                 'American Indian or Alaskan Native'),
                (('Asian (including Chinese, Filipino, Japanese, '
                  + 'Korean, Asian Indian, or Thai)'),
                 ('Asian (including Chinese, Filipino, Japanese, '
                  + 'Korean, Asian Indian, or Thai)')),
                ('Asian (other)', 'Asian (other)'),
                ('Black or African-American',
                 'Black or African-American'),
                ('Native Hawaiian or Pacific Islander',
                 'Native Hawaiian or Pacific Islander'),
                ('White', 'White'),
                ('More Than One Race', 'More Than One Race'),
                ('Other', 'Other'),
                ('Prefer not to answer', 'I prefer not to answer')])
        )
    disadvantaged = forms.CharField(
        label=("Prior to the age of 18, do you feel that you were "
               "educationally or financially disadvantaged?"),
        widget=forms.Select(choices=[('Please Select',
                                      'Please Select'),
                                     ('yes', 'Yes'),
                                     ('no', 'No'),
                                     ('Prefer not to answer',
                                      'I prefer not to answer')])
        )
    employment_location = forms.CharField(
        label="Which category best describes your employment location?",
        widget=forms.Select(
            choices=[('Please Select', 'Please Select'),
                     ('Academia', 'Academia'),
                     ('Federal government', 'Federal government'),
                     ('State government', 'State government'),
                     ('City/County government', 'City/County government'),
                     ('Indian Health/Tribal government',
                      'Indian Health/Tribal government'),
                     ('Hospitals', 'Hospitals'),
                     ('Community-based Organizations/Non-profit',
                      'Community-based Organizations/Non-profit'),
                     ('Private Industry', 'Private Industry'),
                     ('Other', 'Other')])
        )
    position = forms.CharField(
        label="Which general job category best describes your position?",
        widget=forms.Select(
            choices=[
                ('Please Select', 'Please Select'),
                ('Biostatistician', 'Biostatistician'),
                ('Community health worker', 'Community health worker'),
                ('Consumer', 'Consumer'),
                ('Dentist', 'Dentist'),
                ('Elected government official', 'Elected government official'),
                ('Emergency management/bioterrorism preparedness',
                 'Emergency management/bioterrorism preparedness'),
                ('Environmental health/sanitarian',
                 'Environmental health/sanitarian'),
                ('Epidemiology', 'Epidemiology'),
                ('Health administration', 'Health administration'),
                ('Health information systems/data analyst',
                 'Health information systems/data analyst'),
                ('Health promotion/education', 'Health promotion/education'),
                ('Home health aide/medical assistant',
                 'Home health aide/medical assistant'),
                ('Laboratory sciences', 'Laboratory sciences'),
                ('Law enforcement', 'Law enforcement'),
                ('Mental health/substance abuse',
                 'Mental health/substance abuse'),
                ('Nurse', 'Nurse'),
                ('Nutritionist/dietician', 'Nutritionist/dietician'),
                ('Pharmacist', 'Pharmacist'),
                ('Physician', 'Physician'),
                ('Physician assistant', 'Physician assistant'),
                ('Psychologist', 'Psychologist'),
                ('Public health law', 'Public health law'),
                ('Public health policy', 'Public health policy'),
                ('Social worker', 'Social worker'),
                ('Support staff member',
                 ('Support staff member (e.g. administrative assistant, '
                  + 'clerk)')),
                ('Teacher/faculty member', 'Teacher/faculty member'),
                ('Veterinarian', 'Veterinarian'),
                ('Other', 'Other')])
        )
