# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import dj_database_url  # Heroku

from os.path import join
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS


# login required redirect
LOGIN_URL = 'perfiles:login'
# LOGIN_REDIRECT_URL = 'temas/main/recientes' no sirve porque no se usa el login default de django.

#notificaciones
TEMPLATE_CONTEXT_PROCESSORS += ('olibertaria.context_processor_notificaciones.procesar_notificaciones',
                                'olibertaria.context_processor_nickname.procesar_nickname')

#endless pagination
TEMPLATE_CONTEXT_PROCESSORS += ('django.core.context_processors.request',)
ENDLESS_PAGINATION_PER_PAGE = 10
ENDLESS_PAGINATION_PREVIOUS_LABEL = "Anterior"
ENDLESS_PAGINATION_NEXT_LABEL = "Siguiente"


BASE_DIR = os.path.dirname(os.path.dirname(__file__))

TEMPLATE_DIRS = (
    join(BASE_DIR,  'templates'),
)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ["OL_SECRET_KEY"]

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = TEMPLATE_DEBUG = True

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
    'notificaciones',
    'south',
    'social.apps.django_app.default',
    'endless_pagination',
    'gunicorn',
    'storages'
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

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
AWS_ACCESS_KEY_ID = os.environ['AWSAccessKeyId']
AWS_SECRET_ACCESS_KEY = os.environ['AWSSecretKey']
AWS_STORAGE_BUCKET_NAME = os.environ['AWS_STORAGE_BUCKET_NAME']
S3_URL = 'http://%s.s3.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME
STATIC_URL = S3_URL

if not DEBUG:
    SOCIAL_AUTH_FACEBOOK_KEY = os.environ["SOCIAL_AUTH_FACEBOOK_KEY"]
    SOCIAL_AUTH_FACEBOOK_SECRET = os.environ["SOCIAL_AUTH_FACEBOOK_SECRET"]
    SOCIAL_AUTH_TWITTER_KEY = os.environ["SOCIAL_AUTH_TWITTER_KEY"]
    SOCIAL_AUTH_TWITTER_SECRET = os.environ["SOCIAL_AUTH_TWITTER_SECRET"]
    SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.environ["SOCIAL_AUTH_GOOGLE_SECRET"]
    SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.environ["SOCIAL_AUTH_GOOGLE_KEY"]

AUTHENTICATION_BACKENDS = (
    'social.backends.facebook.FacebookOAuth2',
    'social.backends.google.GoogleOAuth2',
    'social.backends.twitter.TwitterOAuth',
    'django.contrib.auth.backends.ModelBackend',
)

TEMPLATE_CONTEXT_PROCESSORS += (
    'social.apps.django_app.context_processors.backends',
    'social.apps.django_app.context_processors.login_redirect',
)

SOCIAL_AUTH_PIPELINE = (
    'social.pipeline.social_auth.social_details',
    'social.pipeline.social_auth.social_uid',
    'social.pipeline.social_auth.auth_allowed',
    'social.pipeline.social_auth.social_user',
    'social.pipeline.user.get_username',
    'social.pipeline.user.create_user',
    'social.pipeline.social_auth.associate_user',
    'social.pipeline.social_auth.load_extra_data',
    'social.pipeline.user.user_details',
    'olibertaria.utils.crear_perfil',
    'olibertaria.utils.obtener_avatar',
    'olibertaria.utils.crear_nickname'
)

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
DATABASES = {}  # Heroku
DATABASES['default'] = dj_database_url.config()  # Heroku

if len(DATABASES['default']) == 0:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'localherokudb',
            'USER': 'alejandro',
            'PASSWORD': os.environ["POSTGRE_PSWD"]
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

#if DEBUG:
#   STATIC_URL = '/static/'

# --- HEROKU --- #
# Parse database configuration from $DATABASE_URL

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

# Static asset configuration
STATIC_ROOT = '/'
