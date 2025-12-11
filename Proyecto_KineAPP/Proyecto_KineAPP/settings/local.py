from .base import *
import os

DEBUG = True

ALLOWED_HOSTS = ["*"]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',   # también vale 'postgresql_psycopg2'
        'NAME': os.environ.get('POSTGRES_DB', 'db_kinesiologia'),
        'USER': os.environ.get('POSTGRES_USER', 'user_kinesiologia'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', 'messironaldo'),
        'HOST': os.environ.get('POSTGRES_HOST', 'localhost'),
        'PORT': os.environ.get('POSTGRES_PORT', '5432'),
    }
}

LOGIN_URL = '/admin/login/'
LOGIN_REDIRECT_URL = '/admin/'
LOGOUT_REDIRECT_URL = '/admin/login/'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = 'no-reply@kinergiaroyale.local'
