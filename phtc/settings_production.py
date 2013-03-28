# flake8: noqa
from settings_shared import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'phtc',
        'HOST': '',
        'PORT': 6432,
        'USER': '',
        'PASSWORD': '',
    }
}

TEMPLATE_DIRS = (
    "/var/www/phtc/phtc/phtc/templates",
)

MEDIA_ROOT = '/var/www/phtc/uploads/'
# put any static media here to override app served static media
STATICMEDIA_MOUNTS = (
    ('/sitemedia', '/var/www/phtc/phtc/sitemedia'),
)

COMPRESS_ROOT = "/var/www/phtc/phtc/media/"
DEBUG = False
TEMPLATE_DEBUG = DEBUG

# unset this to prevent anyone from accidently running pull_from_prod on production
PROD_BASE_URL = None

# IMPORTANT: make sure your local_settings.py file
# has a SENTRY_KEY defined
# as documented in the wiki
SENTRY_SITE = 'phtc'
SENTRY_SERVERS = ['http://sentry.ccnmtl.columbia.edu/sentry/store/']

import logging
from raven.contrib.django.handlers import SentryHandler

logger = logging.getLogger()
# ensure we havent already registered the handler
if SentryHandler not in map(type, logger.handlers):
    logger.addHandler(SentryHandler())

    # Add StreamHandler to sentry's default so you can catch missed exceptions
    logger = logging.getLogger('sentry.errors')
    logger.propagate = False
    logger.addHandler(logging.StreamHandler())

try:
    from local_settings import *
except ImportError:
    pass
