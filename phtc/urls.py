from django.conf import settings
from django.contrib import admin
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
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
    (r'^reports/$', 'phtc.main.views.reports'),
    (r'^admin/', include(admin.site.urls)),
    url(r'^$',
        view='phtc.main.views.dashboard',
        name='dashboard'),
    url(r'^dashboard/',
        view='phtc.main.views.dashboard',
        name='dashboard'),
    (r'^dashboard_panel/',
        'phtc.main.views.dashboard_panel'),
    (r'^help/$',
     'phtc.main.views.help_page'),
    (r'^contact/$',
     'phtc.main.views.contact_page'),
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

)
