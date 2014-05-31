"""
Django settings for olibertaria project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import dj_database_url  # Heroku

from os.path import join
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS

#notificaciones
TEMPLATE_CONTEXT_PROCESSORS += ('olibertaria.context_processor_notificaciones.procesar_notificaciones',)

#endless pagination
TEMPLATE_CONTEXT_PROCESSORS += ('django.core.context_processors.request',)
ENDLESS_PAGINATION_PER_PAGE = 10
ENDLESS_PAGINATION_PREVIOUS_LABEL = "Anterior"
ENDLESS_PAGINATION_NEXT_LABEL = "Siguiente"


#crispy forms
CRISPY_TEMPLATE_PACK = 'bootstrap3'


BASE_DIR = os.path.dirname(os.path.dirname(__file__))

TEMPLATE_DIRS = (
    join(BASE_DIR,  'templates'),
)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'reyd@kps)!ab2z9nu0ok%*es6su51oa$%d3s450c$ksjc&rl1k'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'temas',
    'perfiles',
    'citas',
    'imagenes',
    'videos',
    'django_extensions',
    'south',
    'endless_pagination',
    'crispy_forms',
    'notificaciones',
    #'debug_toolbar',
    'gunicorn',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'olibertaria.urls'

WSGI_APPLICATION = 'olibertaria.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
DATABASES = {}  # Heroku
DATABASES['default'] = dj_database_url.config()  # Heroku

if len(DATABASES['default']) == 0:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'dbolibertaria',
            'USER': 'alejandro',
            'PASSWORD': 'farseer99'
        }
    }

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'es-me'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),)

STATIC_URL = '/static/'

# --- HEROKU --- #
# Parse database configuration from $DATABASE_URL

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

# Static asset configuration
STATIC_ROOT = 'staticfiles'
