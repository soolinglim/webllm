from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

CSRF_TRUSTED_ORIGINS = [ "https://distinctly-lenient-hornet.ngrok-free.app"]

MEDIA_ROOT = os.path.join(BASE_DIR, '..', 'media')

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = False

# for django compressor
COMPRESS_ENABLED = not DEBUG # the default is not DEBUG, toggle for testing
# COMPRESS_ENABLED = DEBUG # the default is not DEBUG, toggle for testing
COMPRESS_ROOT = os.path.join(BASE_DIR, '..', 'static')

