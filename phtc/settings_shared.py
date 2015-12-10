# Django settings for phtc project.
import os.path
import sys
from ccnmtlsettings.shared import common

project = 'phtc'
base = os.path.dirname(__file__)
locals().update(common(project=project, base=base))

ALLOWED_HOSTS = [
    "training.lowernysphtc.org",
    ".ccnmtl.columbia.edu", "localhost"]

USE_TZ = True

INSTALLED_APPS += [  # noqa
    'sorl.thumbnail',
    'tagging',
    'typogrify',
    'bootstrapform',
    'phtc.main',
    'pagetree',
    'pageblocks',
    'quizblock',
    'registration',
    'smartif',
    'treebeard',
    'phtc.treatment_activity',
    'phtc.logic_model',
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

THUMBNAIL_SUBDIR = "thumbs"

PROD_BASE_URL = "http://training.lowernysphtc.org/"
PROD_MEDIA_BASE_URL = "http://training.lowernysphtc.org/uploads/"
