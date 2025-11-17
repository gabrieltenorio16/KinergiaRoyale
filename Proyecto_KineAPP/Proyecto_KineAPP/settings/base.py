from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-tq5zx8xsq2v_1#2*zu#4i30)@%5e78+298=hsa7u%vm5rami=3'


# Application definition

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # aplicaciones propias 
    'applications.usuario.apps.UsuarioConfig',
    'applications.Contenido.apps.ContenidoConfig',
    'applications.curso_y_modulo.apps.CursoYModuloConfig',
    'applications.diagnostico_paciente.apps.DiagnosticoPacienteConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Proyecto_KineAPP.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'Proyecto_KineAPP.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Usar el modelo de usuario personalizado
AUTH_USER_MODEL = 'usuario.Usuario'


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'es-es'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# === CONFIGURACIÓN DE ARCHIVOS ESTÁTICOS ===

# URL base para los archivos estáticos
STATIC_URL = '/static/'

# Carpeta donde colocarás tus archivos estáticos personalizados (CSS, JS, imágenes, etc.)
# Se ubica directamente en la raíz del proyecto (donde está manage.py)
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# Carpeta destino donde Django recopilará todos los archivos estáticos al ejecutar 'collectstatic'
# (No debes crearla manualmente, Django la genera automáticamente)
STATIC_ROOT = BASE_DIR / "staticfiles"

# === CONFIGURACIÓN DE ARCHIVOS DE MEDIA (opcional si usarás carga de imágenes en el admin) ===
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / "media"


JAZZMIN_SETTINGS = {
    "site_title": "KienergiaRoyale",
    "site_header": "Kinergia UCN",
    "welcome_sign": "Bienvenida al Sistema UCN",
    "site_brand": "UCN Kinergia",
    "site_logo": "img/logo_ucn.png",
    "custom_css": "css/admin_custom.css",
    "custom_js": None,
}


## Aplicación de temas y estilos adicionales para Jazzmin (Dashboard de Admin), se pueden modificar según preferencia

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-success",
    "accent": "accent-teal",
    "navbar": "navbar-dark",
    "no_navbar_border": False,
    "navbar_fixed": False,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": False,
    "sidebar": "sidebar-dark-info",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "minty",
    "dark_mode_theme": None,
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success",
    },
}