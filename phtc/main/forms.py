from django import forms
from registration.forms import RegistrationForm
from django.contrib.auth.models import User

attrs_dict = {'class': 'required'}


class UserRegistrationForm(RegistrationForm):
    fname = forms.CharField(
        label="First Name",
        widget=forms.TextInput(attrs={'class': 'fname', 'size': '60'})
        )
    lname = forms.CharField(
        label="Last Name",
        widget=forms.TextInput(attrs={'class': 'lname', 'size': '60'})
        )
    age = forms.CharField(
        label="Select your age group",
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
    sex = forms.CharField(
        max_length=6,
        label="Select your gender.",
        widget=forms.Select(choices=[('Please Select', 'Please Select'),
                                     ('male', 'Male'),
                                     ('female', 'Female')])
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
        label=("Select the option(s) which best represents your race (select all that apply)"),
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
    degree = forms.CharField(
        label=("Select the highest degree earned."),
        widget=forms.Select(choices=[('Please Select', 'Please Select'),
                                     ('High school/GED', 'High school/GED'),
                                     ('Associate degree', 'Associate degree'),
                                     ('Bachelors degree', 'Bachelors degree'),
                                     ('Masters degree', 'Masters Degree'),
                                     ('Doctoral degree or equivalent',
                                      'Doctoral degree or equivalent')])
        )

    work_city = forms.CharField(
        label="Work City",
        widget=forms.TextInput(attrs={'size': '60'})
        )

    work_state = forms.CharField(
        label="Work State",
        widget=forms.Select(
            choices=[('Please Select', 'Please Select'),
                    ('AL', 'Alabama'),
                    ('AK', 'Alaska'),
                    ('AZ', 'Arizona'),
                    ('AR', 'Arkansas'),
                    ('CA', 'California'),
                    ('CO', 'Colorado'),
                    ('CT', 'Connecticut'),
                    ('DE', 'Delaware'),
                    ('DC', 'District of Columbia'),
                    ('FL', 'Florida'),
                    ('GA', 'Georgia'),
                    ('HI', 'Hawaii'),
                    ('ID', 'Idaho'),
                    ('IL', 'Illinois'),
                    ('IN', 'Indiana'),
                    ('IA', 'Iowa'),
                    ('KS', 'Kansas'),
                    ('KY', 'Kentucky'),
                    ('LA', 'Louisiana'),
                    ('ME', 'Maine'),
                    ('MD', 'Maryland'),
                    ('MA', 'Massachusetts'),
                    ('MI', 'Michigan'),
                    ('MN', 'Minnesota'),
                    ('MS', 'Mississippi'),
                    ('MO', 'Missouri'),
                    ('MT', 'Montana'),
                    ('NE', 'Nebraska'),
                    ('NV', 'Nevada'),
                    ('NH', 'New Hampshire'),
                    ('NJ', 'New Jersey'),
                    ('NM', 'New Mexico'),
                    ('NY', 'New York'),
                    ('NC', 'North Carolina'),
                    ('ND', 'North Dakota'),
                    ('OH', 'Ohio'),
                    ('OK', 'Oklahoma'),
                    ('OR', 'Oregon'),
                    ('PA', 'Pennsylvania'),
                    ('RI', 'Rhode Island'),
                    ('SC', 'South Carolina'),
                    ('SD', 'South Dakota'),
                    ('TN', 'Tennessee'),
                    ('TX', 'Texas'),
                    ('UT', 'Utah'),
                    ('VT', 'Vermont'),
                    ('VA', 'Virginia'),
                    ('WA', 'Washington'),
                    ('WV', 'West Virginia'),
                    ('WI', 'Wisconsin'),
                    ('WY', 'Wyoming')])
        )

    work_zip = forms.CharField(
        label="Work Zip Code",
        widget=forms.TextInput(attrs={'size': '60'})
        )

    position = forms.CharField(
        label="Which of the following categories best describes your primary discipline/specialty?",
        widget=forms.Select(
            attrs={'class': 'position-category'},
            choices=[
                ('Please Select', 'Please Select'),
                ('Biostatistics','Biostatistics'),
                ('Behavioral Health |Social Work','Behavioral Health |Social Work'),
                ('Behavioral Health |Psychology','Behavioral Health |Psychology'),
                ('Behavioral Health - Substance use/Addiction Counseling','Behavioral Health - Substance use/Addiction Counseling'),
                ('Community Health Worker','Community Health Worker'),
                ('Dentistry','Dentistry'),
                ('Emergency management/emergency preparedness','Emergency management/emergency preparedness'),
                ('Environmental Health - Environmental chemistry','Environmental Health - Environmental chemistry'),
                ('Environmental Health - Environmental health planning','Environmental Health - Environmental health planning'),
                ('Environmental Health - Environmental sciences','Environmental Health - Environmental sciences'),
                ('Environmental Health - Industrial hygiene','Environmental Health - Industrial hygiene'),
                ('Environmental Health - Occupational safety and health','Environmental Health - Occupational safety and health'),
                ('Environmental Health - Radiological health','Environmental Health - Radiological health'),
                ('Environmental Health - Toxicology','Environmental Health - Toxicology'),
                ('Environmental Health - Water quality','Environmental Health - Water quality'),
                ('Epidemiology','Epidemiology'),
                ('EMT-Paramedic/First responder','EMT-Paramedic/First responder'),
                ('Geriatrics/Aging Populations','Geriatrics/Aging Populations'),
                ('Global/International Health - Tropical medicine','Global/International Health - Tropical medicine'),
                ('Health education/behavior - Behavioral sciences','Health education/behavior - Behavioral sciences'),
                ('Health education/behavior - Community health sciences','Health education/behavior - Community health sciences'),
                ('Health education/behavior - Evaluation research','Health education/behavior - Evaluation research'),
                ('Health education/behavior - Health behavior','Health education/behavior - Health behavior'),
                ('Health education/behavior - Health promotion/disease prevention','Health education/behavior - Health promotion/disease prevention'),
                ('Health Policy/Law','Health Policy/Law'),
                ('Health Services Research','Health Services Research'),
                ('Health Services/Hospital Administration','Health Services/Hospital Administration'),
                ('Health Services/Hospital Administration - Health management','Health Services/Hospital Administration - Health management'),
                ('Health Services/Hospital Administration - Health planning','Health Services/Hospital Administration - Health planning'),
                ('Health Services/Hospital Administration - Hospital administration','Health Services/Hospital Administration - Hospital administration'),
                ('Maternal & Child Health - Adolescent health','Maternal & Child Health - Adolescent health'),
                ('Maternal & Child Health - Infant and child health','Maternal & Child Health - Infant and child health'),
                ('Maternal & Child Health - Womens health','Maternal & Child Health - Womens health'),
                ('Medicine - Physician','Medicine - Physician'),
                ('Medicine - Physician Assistant','Medicine - Physician Assistant'),
                ('Nutrition - Dietetics','Nutrition - Dietetics'),
                ('Nutrition - Public health nutrition','Nutrition - Public health nutrition'),
                ('Nursing - Advanced nurse specialist','Nursing - Advanced nurse specialist'),
                ('Nursing - Home health aide','Nursing - Home health aide'),
                ('Nursing - Nurse Practitioner (NP)','Nursing - Nurse Practitioner (NP)'),
                ('Nursing - Patient Care Associate (PCA)','Nursing - Patient Care Associate (PCA)'),
                ('Nursing - Registered nurse (RN)','Nursing - Registered nurse (RN)'),
                ('Nursing - Occupational Health','Nursing - Occupational Health'),
                ('Pharmacy','Pharmacy'),
                ('Public Health (general studies)','Public Health (general studies)'),
                ('Public Health Practice - Community health practice','Public Health Practice - Community health practice'),
                ('Public Health Practice - Program management','Public Health Practice - Program management'),
                ('Support staff','Support staff'),
                ('Urban Health','Urban Health'),
                ('Other', 'Other')])
        )
    other_position_category = forms.CharField(
        required=False,
        label="Please Specify",
        widget=forms.TextInput(attrs={'class': 'position-category-input',
                                      'size': '60'})
        )

    employment_location = forms.CharField(
        label="Which category best describes your employment location?",
        widget=forms.Select(
            attrs={'class': 'employment-location'},
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

    other_employment_location = forms.CharField(
        required=False,
        label="Please Specify",
        widget=forms.TextInput(attrs={'class': 'employment-location-input',
                                      'size': '60'})
        )

    dept_health = forms.CharField(
        label="Do you work in a department of public health?",
        widget=forms.Select(
            choices=[('Please Select', 'Please Select'),
                     ('Yes', 'Yes'),
                     ('No', 'No'),
                     ('I do not know', 'I do not know')])
        )
    geo_dept_health = forms.CharField(
        label=("Do you work in a health department within our target "
               "geographic area?"),
        widget=forms.Select(
            choices=[('Please Select', 'Please Select'),
                     ('Putnam County (NY)', 'Putnam County (NY)'),
                     ('Westchester County (NY)', 'Westchester County (NY)'),
                     ('Nassau County (NY)', 'Nassau County (NY)'),
                     ('Suffolk County (NY)', 'Suffolk County (NY)'),
                     ('New York City (NY)', 'New York City (NY)'),
                     ('I do not work in any of the health departments listed',
                      'I do not work in any of the health departments listed')
                     ])
        )

    experience = forms.CharField(
        label="How many years have you worked in public health?",
        widget=forms.Select(
            choices=[('Please Select', 'Please Select'),
                     ('0-5', '0-5'),
                     ('6-10', '6-10'),
                     ('11-15', '11-15'),
                     ('16-20', '16-20'),
                     ('21-25', '21-25'),
                     ('25+', '25+'),
                     ('I do not work in public health',
                      'I do not work in public health')])
        )

    umc = forms.CharField(
        label="Do you work in a medically underserved community (MUC)?",
        widget=forms.Select(
            choices=[('Please Select', 'Please Select'),
                     ('Yes', 'Yes'),
                     ('No', 'No'),
                     ('I do not know', 'I do not konw')])
        )

    rural = forms.CharField(
        label="Do you work in a rural setting?",
        widget=forms.Select(
            choices=[('Please Select', 'Please Select'),
                     ('Yes', 'Yes'),
                     ('No', 'No'),
                     ('I do not know', 'I do not konw')])
        )

    is_nylearns = forms.BooleanField(
        required=False,
        widget = forms.HiddenInput(),
        initial = False
        )

    nylearns_username = forms.CharField(
        required = False,
        widget = forms.HiddenInput(),
        initial = "none"
        )

    nylearns_user_id = forms.CharField(
        required = False,
        widget = forms.HiddenInput(),
        initial = "none"
        )

    nylearns_course_init = forms.CharField(
        required = False,
        widget = forms.HiddenInput(),
        initial = "none"
        )

    def clean_email(self):
      data = self.cleaned_data['email']
      if User.objects.filter(email=data).exists():
          raise forms.ValidationError("This email is already in use. Are you sure that you don't already have an account?")
      return data

