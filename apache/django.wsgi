import os, sys, site

# enable the virtualenv
site.addsitedir('/var/www/phtc/phtc/ve/lib/python2.6/site-packages')

# paths we might need to pick up the project's settings
sys.path.append('/var/www/phtc/phtc/')

os.environ['DJANGO_SETTINGS_MODULE'] = 'phtc.settings_production'

import django.core.handlers.wsgi
import django
django.setup()
application = django.core.handlers.wsgi.WSGIHandler()
