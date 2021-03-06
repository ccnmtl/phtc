# flake8: noqa
from phtc.settings_shared import *
from ccnmtlsettings.staging import common

locals().update(
    common(
        project=project,
        base=base,
        STATIC_ROOT=STATIC_ROOT,
        INSTALLED_APPS=INSTALLED_APPS,
        s3static=True,
    ))

PROD_BASE_URL = None

try:
    from phtc.local_settings import *
except ImportError:
    pass

