import django.contrib.auth.views
import django.views.static
import djangowind.views

from django.conf import settings
from django.contrib import admin
from django.conf.urls import include, url
from django.views.generic import TemplateView

from phtc.main.views import (
    region2phtc, dashboard, edit_page, page,
)
admin.autodiscover()

redirect_after_logout = getattr(settings, 'LOGOUT_REDIRECT_URL', None)
auth_urls = url(r'^accounts/', include('django.contrib.auth.urls'))
logout_page = url(r'^accounts/logout/$', django.contrib.auth.views.logout,
                  {'next_page': redirect_after_logout})

if hasattr(settings, 'CAS_BASE'):
    auth_urls = url(r'^accounts/', include('djangowind.urls'))
    logout_page = url(r'^accounts/logout/$', djangowind.views.logout,
                      {'next_page': redirect_after_logout})

urlpatterns = [
    logout_page,
    auth_urls,
    url(r'^$', view=region2phtc, name='region2phtc'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^dashboard/', view=dashboard, name='dashboard'),
    url(r'^_stats/', TemplateView.as_view(template_name='stats.html')),
    url(r'^uploads/(?P<path>.*)$', django.views.static.serve,
        {'document_root': settings.MEDIA_ROOT}),
    url(r'^_pagetree/', include('pagetree.urls')),
    url(r'^_quiz/', include('quizblock.urls')),
    url(r'^_rgt/', include('phtc.treatment_activity.urls')),
    url(r'^_logic_model/', include('phtc.logic_model.urls')),
    url(r'^smoketest/', include('smoketest.urls')),
    # these need to be last
    url(r'^edit/(?P<path>.*)$', edit_page, {}, 'edit-page'),
    url(r'^(?P<path>.*)$', page),
]
