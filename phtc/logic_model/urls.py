from django.conf.urls import patterns, url
import os.path

media_root = os.path.join(os.path.dirname(__file__), "media")

urlpatterns = patterns(
    '',
    (r'^media/(?P<path>.*)$', 'django.views.static.serve',
     {'document_root': media_root}),

    url(r'^settings/$',
        'phtc.logic_model.views.settings',
        name='settings'),
)
