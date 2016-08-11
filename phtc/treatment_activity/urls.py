import django.views.static
import os.path
from django.conf.urls import url

from .views import choose_treatment_path, get_next_steps


media_root = os.path.join(os.path.dirname(__file__), "media")

urlpatterns = [
    url(r'^media/(?P<path>.*)$', django.views.static.serve,
        {'document_root': media_root}),
    url(r'^$', choose_treatment_path, name='choose-treatment-path'),
    url(r'^(?P<path_id>\d+)/(?P<node_id>\d+)/$', get_next_steps,
        name="get-next-steps"),
]
