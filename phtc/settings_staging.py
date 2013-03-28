# flake8: noqa
from settings_shared import *

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
STAGING_ENV = True
TEMPLATE_DEBUG = DEBUG

PROD_BASE_URL = None

SENTRY_SITE = 'phtc-staging'
STATSD_PREFIX = 'phtc-staging'

SENTRY_SERVERS = ['http://sentry.ccnmtl.columbia.edu/sentry/store/']

if 'migrate' not in sys.argv:
    import logging
    from raven.contrib.django.handlers import SentryHandler

    logger = logging.getLogger()
    # ensure we havent already registered the handler
    if SentryHandler not in map(type, logger.handlers):
        logger.addHandler(SentryHandler())
        logger = logging.getLogger('sentry.errors')
        logger.propagate = False
        logger.addHandler(logging.StreamHandler())

try:
    from local_settings import *
except ImportError:
    pass
