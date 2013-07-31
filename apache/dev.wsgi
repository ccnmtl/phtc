import os, sys, site

sys.path.append('/var/www/phtc/phtc/')

os.environ['DJANGO_SETTINGS_MODULE'] = 'phtc.settings_dev'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()
