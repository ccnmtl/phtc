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
TEMPLATE_DEBUG = DEBUG

# unset this to prevent anyone from accidently running pull_from_prod on production
PROD_BASE_URL = None

try:
    from local_settings import *
except ImportError:
    pass
