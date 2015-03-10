import os, sys, site

sys.path.append('/var/www/phtc/phtc/')

os.environ['DJANGO_SETTINGS_MODULE'] = 'phtc.settings_staging'

import django.core.handlers.wsgi
import django
django.setup()
application = django.core.handlers.wsgi.WSGIHandler()
