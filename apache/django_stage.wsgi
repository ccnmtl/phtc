import os, sys, site

# enable the virtualenv

site.addsitedir('/usr/local/share/sandboxes/common/phtc/phtc/ve/lib/python2.6/site-packages')

# paths we might need to pick up the project's settings
sys.path.append('/usr/local/share/sandboxes/common/')
sys.path.append('/usr/local/share/sandboxes/common/phtc/')
sys.path.append('/usr/local/share/sandboxes/common/phtc/phtc/')

os.environ['DJANGO_SETTINGS_MODULE'] = 'phtc.settings_stage'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()
