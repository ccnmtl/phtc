import os.path
from django.conf.urls import patterns, url


media_root = os.path.join(os.path.dirname(__file__), "media")

urlpatterns = patterns(
    '',
    (r'^media/(?P<path>.*)$', 'django.views.static.serve',
     {'document_root': media_root}),
    url(r'^$',
        'phtc.treatment_activity.views.choose_treatment_path',
        name='choose-treatment-path'),
    url(r'^(?P<path_id>\d+)/(?P<node_id>\d+)/$',
        'phtc.treatment_activity.views.get_next_steps',
        name="get-next-steps"),
)
