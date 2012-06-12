from django.conf.urls.defaults import patterns, include, url
from registration.views import register
from django.contrib import admin
from django.conf import settings
from django.views.generic.simple import direct_to_template
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

urlpatterns = patterns('',
                       auth_urls,
                       logout_page,
                       url(r'^registration/register/$',
                           register,
                           {'backend':
                            'registration.backends.default.DefaultBackend',
                            'form_class': UserRegistrationForm},
                        name='registration_register'),
                       (r'^registration/', include('registration.urls')),
                       (r'^admin/', include(admin.site.urls)),
                       (r'^munin/', include('munin.urls')),
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
                       (r'^_export/', 'phtc.main.views.exporter'),
                       # these need to be last
                       (r'^edit/(?P<path>.*)$', 'phtc.main.views.edit_page',
                        {}, 'edit-page'),
                       (r'^instructor/(?P<path>.*)$',
                        'phtc.main.views.instructor_page'),
                       (r'^(?P<path>.*)$', 'phtc.main.views.page'),

) + staticmedia.serve()
