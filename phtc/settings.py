# flake8: noqa
from phtc.settings_shared import *

try:
    from phtc.local_settings import *
except ImportError:
    pass
