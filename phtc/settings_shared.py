# Django settings for phtc project.
import os.path
import sys

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = ()

MANAGERS = ADMINS

ALLOWED_HOSTS = [
    "training.lowernysphtc.org",
    ".ccnmtl.columbia.edu", "localhost"]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'phtc',
        'HOST': '',
        'PORT': 5432,
        'USER': '',
        'PASSWORD': '',
    }
}

USE_TZ = True
TIME_ZONE = 'America/New_York'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = False
MEDIA_ROOT = "/var/www/phtc/uploads/"
MEDIA_URL = '/uploads/'
STATIC_URL = '/media/'
STATICFILES_DIRS = (
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../media/")),
)
STATIC_ROOT = "/media/"
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

COMPRESS_URL = "/media/"
COMPRESS_ROOT = "media/"

SECRET_KEY = ')ng#)ef_u@_^zvvu@dxm7ql-yb^_!a6%v3v^j3b(mp+)l+5%@h'
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'djangowind.context.context_processor',
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.request',
    'django.core.context_processors.static',
    'stagingcontext.staging_processor',

)

MIDDLEWARE_CLASSES = (
    'django_statsd.middleware.GraphiteRequestTimingMiddleware',
    'django_statsd.middleware.GraphiteMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'phtc.urls'

TEMPLATE_DIRS = (
    # Put application templates before these fallback ones:
    "/var/www/phtc/templates/",
    os.path.join(os.path.dirname(__file__), "templates"),
    os.path.join(os.path.dirname(__file__),
                 "../ve/lib/python2.7/site-packages/treebeard/templates"),
)

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sites',
    'django.contrib.flatpages',
    'django.contrib.staticfiles',
    'sorl.thumbnail',
    'django.contrib.admin',
    'tagging',
    'typogrify',
    'raven.contrib.django',
    'south',
    'django_nose',
    'compressor',
    'django_statsd',
    'bootstrapform',
    'phtc.main',
    'pagetree',
    'pageblocks',
    'quizblock',
    'registration',
    'debug_toolbar',
    'smartif',
    'django_jenkins',
    'treebeard',
    'phtc.treatment_activity',
    'phtc.logic_model',
    'django_markwhat',
    'smoketest',
]

LETTUCE_APPS = (
    'phtc.main',
)
LETTUCE_SERVER_PORT = 7000

ACCOUNT_ACTIVATION_DAYS = 7
AUTH_PROFILE_MODULE = "phtc.main.UserProfile"
SERVER_EMAIL = ("NYC-LI-LTC Public Health Training Center "
                "<no-reply@lowernysphtc.org>")
DEFAULT_FROM_EMAIL = ("NYC-LI-LTC Public Health Training Center "
                      "<no-reply@lowernysphtc.org>")

PAGEBLOCKS = ['pageblocks.TextBlock',
              'pageblocks.HTMLBlock',
              'pageblocks.PullQuoteBlock',
              'pageblocks.ImageBlock',
              'pageblocks.ImagePullQuoteBlock',
              'quizblock.Quiz',
              'treatment_activity.TreatmentActivityBlock',
              'logic_model.LogicModelBlock'
              ]


STATSD_CLIENT = 'statsd.client'
STATSD_PREFIX = 'phtc'
STATSD_HOST = '127.0.0.1'
STATSD_PORT = 8125
STATSD_PATCHES = []

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
if 'test' in sys.argv or 'jenkins' in sys.argv:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
            'HOST': '',
            'PORT': '',
            'USER': '',
            'PASSWORD': '',
        }
    }
    COMPRESS_ENABLED = False

NOSE_ARGS = [
    '--with-coverage',
    '--cover-package=phtc',
]

JENKINS_TASKS = (
    'django_jenkins.tasks.run_pylint',
    'django_jenkins.tasks.with_coverage',
    'django_jenkins.tasks.run_pep8',
    'django_jenkins.tasks.run_pyflakes',
)

PROJECT_APPS = ['phtc.main', 'quizblock', 'phtc.logic_model',
                'phtc.treatment_activity']

if 'harvest' in sys.argv:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'lettuce.db',
            'HOST': '',
            'PORT': '',
            'USER': '',
            'PASSWORD': '',
        }
    }


SOUTH_TESTS_MIGRATE = False

THUMBNAIL_SUBDIR = "thumbs"
EMAIL_SUBJECT_PREFIX = "[phtc] "
EMAIL_HOST = 'localhost'
SERVER_EMAIL = "phtc@ccnmtl.columbia.edu"

COMPRESS_URL = "/media/"
COMPRESS_ROOT = "media/"
COMPRESS_PARSER = "compressor.parser.HtmlParser"

# WIND settings

AUTHENTICATION_BACKENDS = ('djangowind.auth.SAMLAuthBackend',
                           'django.contrib.auth.backends.ModelBackend',)
CAS_BASE = "https://cas.columbia.edu/"
LOGOUT_REDIRECT_URL = "https://cas.columbia.edu/cas/logout"
WIND_PROFILE_HANDLERS = ['djangowind.auth.CDAPProfileHandler']
WIND_AFFIL_HANDLERS = ['djangowind.auth.AffilGroupMapper',
                       'djangowind.auth.StaffMapper',
                       'djangowind.auth.SuperuserMapper']
WIND_STAFF_MAPPER_GROUPS = ['tlc.cunix.local:columbia.edu']
WIND_SUPERUSER_MAPPER_GROUPS = ['anp8', 'jb2410', 'zm4', 'egr2107', 'amm8',
                                'mar227', 'jed2161']

SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"
SESSION_COOKIE_HTTPONLY = True

INTERNAL_IPS = ('127.0.0.1',)

DEBUG_TOOLBAR_PANELS = (
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.signals.SignalsPanel',
)

PROD_BASE_URL = "http://training.lowernysphtc.org/"
PROD_MEDIA_BASE_URL = "http://training.lowernysphtc.org/uploads/"
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTOCOL', 'https')
