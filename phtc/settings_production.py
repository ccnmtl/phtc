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

STATICFILES_DIRS = ()
STATIC_ROOT = os.path.join(os.path.dirname(__file__), "../media")
COMPRESS_ROOT = "/var/www/phtc/phtc/media/"
DEBUG = False
TEMPLATE_DEBUG = DEBUG

# unset this to prevent anyone from accidently running pull_from_prod on production
PROD_BASE_URL = None

if 'migrate' not in sys.argv:
    INSTALLED_APPS.append('raven.contrib.django.raven_compat')

try:
    from local_settings import *
except ImportError:
    pass
