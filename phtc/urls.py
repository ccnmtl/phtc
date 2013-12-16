from django.conf.urls.defaults import patterns, include, url
from registration.views import RegistrationView
from django.contrib import admin
from django.conf import settings
from django.views.generic.simple import direct_to_template
from django.views.generic.simple import redirect_to
import os.path
admin.autodiscover()
import staticmedia
from phtc.main.forms import UserRegistrationForm

site_media_root = os.path.join(os.path.dirname(__file__), "../media")

redirect_after_logout = getattr(settings, 'LOGOUT_REDIRECT_URL', None)
auth_urls = (r'^accounts/', include('django.contrib.auth.urls'))
logout_page = (r'^accounts/logout/$', 'django.contrib.auth.views.logout',
               {'next_page': redirect_after_logout})
if hasattr(settings, 'WIND_BASE'):
    auth_urls = (r'^accounts/', include('djangowind.urls'))
    logout_page = (r'^accounts/logout/$', 'djangowind.views.logout',
                   {'next_page': redirect_after_logout})

urlpatterns = patterns(
    '',
    auth_urls,
    logout_page,
    url(r'^registration/register/$',
        RegistrationView.as_view(form_class=UserRegistrationForm),
        name='registration_register'),
    (r'^registration/', include('registration.urls')),
    (r'^test_nylearns_username/$', 'phtc.main.views.test_nylearns_username'),
    (r'^create_nylearns_user/$', 'phtc.main.views.create_nylearns_user'),
    (r'^nylearns_login/$', 'phtc.main.views.nylearns_login'),
    (r'^nylearns/$', 'phtc.main.views.nylearns'),
    (r'^profile/$', 'phtc.main.views.get_user_profile'),
    (r'^update_profile/$',
     'phtc.main.views.update_user_profile'),
    (r'^reports/$', 'phtc.main.views.reports'),
    (r'^admin/', include(admin.site.urls)),
    (r'^munin/', include('munin.urls')),
    (r'^accounts/profile/$', redirect_to,
     {'url': '/dashboard/'}),
    url(r'^dashboard/',
        view='phtc.main.views.dashboard',
        name='dashboard'),
    (r'^dashboard_panel/',
     'phtc.main.views.dashboard_panel'),
    (r'^about/$',
     'phtc.main.views.about_page'),
    (r'^help/$',
     'phtc.main.views.help_page'),
    (r'^contact/$',
     'phtc.main.views.contact_page'),
    (r'^certificate/(?P<path>.*)$',
     'phtc.main.views.certificate'),
    (r'^_stats/', direct_to_template,
     {'template': 'stats.html'}),
    (r'^site_media/(?P<path>.*)$',
     'django.views.static.serve',
     {'document_root': site_media_root}),
    (r'^uploads/(?P<path>.*)$',
     'django.views.static.serve',
     {'document_root': settings.MEDIA_ROOT}),
    (r'^_pagetree/', include('pagetree.urls')),
    (r'^_quiz/', include('quizblock.urls')),
    (r'^_rgt/', include('phtc.treatment_activity.urls')),
    (r'^_logic_model/', include('phtc.logic_model.urls')),
    # these need to be last
    (r'^edit/(?P<path>.*)$', 'phtc.main.views.edit_page',
     {}, 'edit-page'),
    (r'^instructor/(?P<path>.*)$',
     'phtc.main.views.instructor_page'),
    (r'^(?P<path>.*)$', 'phtc.main.views.page'),
) + staticmedia.serve()
