# settings/local.py

from .base import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

INSTALLED_APPS += ("debug_toolbar", "django_extensions", "south",)
