from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']

CSRF_TRUSTED_ORIGINS=[]

INSTALLED_APPS += (
    'gunicorn',
)

MEDIA_ROOT = '/var/www/media/'
STATIC_ROOT = '/var/www/static/'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_SSL = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = SERVER_EMAIL
EMAIL_HOST_PASSWORD = os.environ["EMAIL_PASSWORD"]
EMAIL_PORT = 465

# for django compressor
COMPRESS_ENABLED = not DEBUG # the default is not DEBUG, toggle for testing
COMPRESS_OFFLINE = True
