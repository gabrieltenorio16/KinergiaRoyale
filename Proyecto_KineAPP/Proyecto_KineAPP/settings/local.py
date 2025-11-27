from .base import *

DEBUG = True
ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'db_kinesiologia',
        'USER': 'user_kinesiologia',
        'PASSWORD': 'messironaldo',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

LOGIN_URL = '/admin/login/'
LOGIN_REDIRECT_URL = '/admin/'
LOGOUT_REDIRECT_URL = '/admin/login/'

# === CORREO SOLO A CONSOLA (DESARROLLO) ===
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = 'no-reply@kinergiaroyale.local'
