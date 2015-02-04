from django.conf.urls import patterns, include, url
from registration.backends.default.views import RegistrationView
from phtc.main.forms import UserRegistrationForm


class RegistrationView(RegistrationView):
    form_class = UserRegistrationForm

from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.views.generic import TemplateView
from django.views.generic import RedirectView
admin.autodiscover()

redirect_after_logout = getattr(settings, 'LOGOUT_REDIRECT_URL', None)
auth_urls = (r'^accounts/', include('django.contrib.auth.urls'))
logout_page = (r'^accounts/logout/$', 'django.contrib.auth.views.logout',
               {'next_page': redirect_after_logout})
admin_logout_page = (r'^accounts/logout/$',
                     'django.contrib.auth.views.logout',
                     {'next_page': '/admin/'})

if hasattr(settings, 'CAS_BASE'):
    auth_urls = (r'^accounts/', include('djangowind.urls'))
    logout_page = (r'^accounts/logout/$', 'djangowind.views.logout',
                   {'next_page': redirect_after_logout})
    admin_logout_page = (r'^admin/logout/$',
                         'djangowind.views.logout',
                         {'next_page': redirect_after_logout})

urlpatterns = patterns(
    '',
    logout_page,
    admin_logout_page,
    auth_urls,
    url(r'^registration/register/$', RegistrationView.as_view(),
        name='registration_register'),
    (r'^register/complete/$', RedirectView.as_view(url='/dashboard/')),
    (r'^registration/', include('registration.backends.default.urls')),

    url(r'^activate/complete/$', TemplateView.as_view(
        template_name='registration/activation_complete.html'),
        name='registration_activation_complete'),
    (r'^test_nylearns_username/$', 'phtc.main.views.test_nylearns_username'),
    (r'^create_nylearns_user/$', 'phtc.main.views.create_nylearns_user'),
    (r'^nylearns_login/$', 'phtc.main.views.nylearns_login'),
    (r'^nylearns/$', 'phtc.main.views.nylearns'),
    (r'^profile/$', 'phtc.main.views.get_user_profile'),
    (r'^update_profile/$',
     'phtc.main.views.update_user_profile'),
    (r'^reports/$', 'phtc.main.views.reports'),
    (r'^admin/', include(admin.site.urls)),
    (r'^accounts/profile/$', RedirectView.as_view(url='/dashboard/')),
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
    (r'^_stats/', TemplateView.as_view(template_name='stats.html')),
    (r'^uploads/(?P<path>.*)$',
     'django.views.static.serve',
     {'document_root': settings.MEDIA_ROOT}),
    (r'^_pagetree/', include('pagetree.urls')),
    (r'^_quiz/', include('quizblock.urls')),
    (r'^_rgt/', include('phtc.treatment_activity.urls')),
    (r'^_logic_model/', include('phtc.logic_model.urls')),
    (r'^smoketest/', include('smoketest.urls')),
    # these need to be last
    (r'^edit/(?P<path>.*)$', 'phtc.main.views.edit_page',
     {}, 'edit-page'),
    (r'^instructor/(?P<path>.*)$',
     'phtc.main.views.instructor_page'),
    (r'^(?P<path>.*)$', 'phtc.main.views.page'),

    #override the default urls for pasword
    url(r'^password/change/$',
        auth_views.password_change,
        name='password_change'),
    url(r'^password/change/done/$',
        auth_views.password_change_done,
        name='password_change_done'),
    url(r'^password/reset/$',
        auth_views.password_reset,
        name='password_reset'),
    url(r'^password/reset/done/$',
        auth_views.password_reset_done,
        name='password_reset_done'),
    url(r'^password/reset/complete/$',
        auth_views.password_reset_complete,
        name='password_reset_complete'),
    url(r'^password/reset/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        auth_views.password_reset_confirm,
        name='password_reset_confirm'),

    #and now add the registration urls
    url(r'', include('registration.backends.default.urls')),
)
