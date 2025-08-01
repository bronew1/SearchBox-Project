"""
Django settings for backend project.

Generated by 'django-admin startproject' using Django 5.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""
import dj_database_url
from pathlib import Path

import os
from dotenv import load_dotenv

load_dotenv()

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "localhost").split(",")
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-tmkple-p1pbf*-xj@b)8qr&)9tfb89d4p&3i=!x4j1#h96_bwv'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    'searchbox-project.onrender.com',
    'localhost',
    '127.0.0.1',
    'www.searchprojectdemo.com',
    'searchprojectdemo.com',
    'www.sinapirlanta.com',  # <--- BUNU EKLE
    'sinapirlanta.com'       # <--- VE BUNU DA
]



# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'products',
    'corsheaders',
    'recommendations',
    'analytics',
    'tracking',
    'campains',
    'rest_framework',
    'subscriptions',
    'webPush',
    'ai_generator',

  
    
]

MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',  # bu satırı en üstte ekle
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates'
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'backend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': dj_database_url.config(default=os.getenv("DATABASE_URL"))
}

# Max 10MB dosya yüklemeye izin ver
DATA_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static")  # ✅ Kendi kaynak klasörün
]

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # ✅ collectstatic buraya kopyalar

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# settings.py


CORS_ALLOW_ALL_ORIGINS = True  # (Geliştirme için OK)

CORS_ALLOWED_ORIGINS = [
    "https://www.searchprojectdemo.com",
    "https://searchprojectdemo.com",
    "https://searchbox-project.onrender.com",
    "https://www.sinapirlanta.com",  # <--- BUNU EKLE
    "https://sinapirlanta.com",      # <--- BUNU DA EKLE
]

CORS_ALLOW_CREDENTIALS = True


# settings.py

BREVO_API_KEY = os.environ.get("BREVO_API_KEY")


EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp-relay.brevo.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "8e19eb004@smtp-brevo.com"     # ✅ Brevo SMTP username
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = "no-reply@sinapirlanta.email"


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        'subscriptions': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

WEBPUSH_SETTINGS = {
    "VAPID_PUBLIC_KEY": os.getenv("VAPID_PUBLIC_KEY"),
    "VAPID_PRIVATE_KEY": os.getenv("VAPID_PRIVATE_KEY"),
    "VAPID_ADMIN_EMAIL": "mailto:berk@example.com"
}



VAPID_PUBLIC_KEY = os.getenv("VAPID_PUBLIC_KEY")
VAPID_PRIVATE_KEY = os.getenv("VAPID_PRIVATE_KEY")



OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

STABILITY_API_KEY = os.getenv("STABILITY_API_KEY")