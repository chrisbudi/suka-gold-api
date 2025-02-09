"""
Django settings for app project.

Generated by 'django-admin startproject' using Django 4.0.10.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

import os
from pathlib import Path
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-(&h@k#kwnn%=m+o8nd()-ck0a$5k)nlpfu1nh@n5-12#+#kcxq"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
# <editor-fold desc="Description">
USE_HTTPS = os.getenv("USE_HTTPS", "false").lower() == "true"
if USE_HTTPS:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
else:
    SECURE_SSL_REDIRECT = False
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False
# </editor-fold>

ALLOWED_HOSTS = [
    "52.221.181.88",
    "127.0.0.1",
    "localhost",
    "172.18.0.1",
    "3.0.17.240",
    "18.138.179.185",
    "nemas.id:8000",
]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "drf_spectacular",
    "rest_framework",
    "rest_framework.authentication",
    "rest_framework_simplejwt",
    "django_filters",
    "django_celery_beat",
    "django_celery_results",
    "channels",
    "taggit",
    "corsheaders",
    "core",
    "user",
    "wallet",
    "gold_transaction",
    "investment",
    "loan",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "corsheaders.middleware.CorsMiddleware",
]

CORS_ALLOWED_ORIGINS = [
    "https://localhost:5005",
    "http://localhost:3000",
    "https://52.221.181.88:5005",
    "https://172.18.0.1",
    "https://18.138.179.185:5005",
    "https://nemas-admin.vercel.app",
    "https://nemas.vercel.app",
    "https://nemas.id:8000",
]


ROOT_URLCONF = "app.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "app.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": os.environ.get("DB_HOST"),
        "NAME": os.environ.get("DB_NAME"),
        "USER": os.environ.get("DB_USER"),
        "PASSWORD": os.environ.get("DB_PASS"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Bangkok"

USE_I18N = True

USE_TZ = True

HTTPCACHE_ENABLED = False
if USE_HTTPS:
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "verbose": {
                "format": "{levelname} {asctime} {module} {message}",
                "style": "{",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "verbose",
            },
            "file": {
                "class": "logging.FileHandler",
                "filename": "api_errors.log",
                "formatter": "verbose",
            },
        },
        "loggers": {
            "django": {
                "handlers": ["console", "file"],
                "level": "INFO",
                "propagate": True,
            },
            "django.request": {
                "handlers": ["console", "file"],
                "level": "ERROR",
                "propagate": False,
            },
            "django.db.backends": {
                "handlers": ["console", "file"],
                "level": "DEBUG",
                "propagate": False,
            },
        },
    }


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "user.user"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}


SPECTACULAR_SETTINGS = {
    "TITLE": "NEMAS API",
    "DESCRIPTION": "Apps backend for nemas",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "COMPONENT_SPLIT_REQUEST": True,
    "SWAGGER_UI_SETTINGS": {
        "deepLinking": True,
    },
    "SECURITY": [{"BearerAuth": []}],
    "AUTHENTICATION_WHITELIST": [
        "rest_framework_simplejwt.authentication.JWTAuthentication"
    ],
    "SCHEMA_PATH_PREFIX": r"",
    "SERVERS": [{"url": "/"}],
    "ENABLE_API_DOCS": True,
    "EXCLUDE_PATHS": ["/admin"],
    "SERVE_PUBLIC": True,
    "OAS_VERSION": "3.0.0",
    "SECURITY_DEFINITIONS": {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        },
    },
}

AUTHENTICATION_BACKENDS = [
    "user.domain.services.UsernameEmailPhoneBackend",
    # "django.contrib.auth.backends.ModelBackend",  # Default backend
]

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": True,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": None,
    "AUDIENCE": None,
    "ISSUER": None,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "JTI_CLAIM": "jti",
}


# S3Config
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"


CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.getenv("CACHE_LOCATION"),  # Redis database 1
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            # Optional: password if Redis requires authentication
            # "PASSWORD": "your_redis_password",
        },
        "KEY_PREFIX": "nemas",
    }
}

# Add these settings to configure S3 storage
AWS_S3 = {
    "ACCESS_KEY_ID": os.getenv("AWS_ACCESS_KEY_ID"),
    "SECRET_ACCESS_KEY": os.getenv("AWS_SECRET_ACCESS_KEY"),
    "BUCKET_NAME": os.getenv("AWS_STORAGE_BUCKET_NAME"),
    "REGION_NAME": os.getenv("AWS_S3_REGION_NAME", "us-east-1"),
    "CUSTOM_DOMAIN": f"{os.getenv('AWS_STORAGE_BUCKET_NAME')}.s3.ap-southeast-1.amazonaws.com",
}
# celery settings
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
CELERY_RESULT_BACKEND = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/1")
CELERY_ACCEPT_CONTENT = ["json"]  # Use JSON for task serialization
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_RESULT_EXTENDED = True  # Optional: Enable extended result info
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 300
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True

# Channels config
ASGI_APPLICATION = "app.asgi.application"


# Redis configuration
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = os.getenv("REDIS_PORT", 6379)
REDIS_DB = os.getenv("REDIS_DB", 0)
REDIS_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", "")

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [os.getenv("REDIS_URL", "redis://127.0.0.1:6379")],
        },
    },
}


VERIHUB = {
    "CLIENT_URL": os.getenv("VERIHUB_CLIENT_URL"),
    "CLIENT_TOKEN": os.getenv("VERIHUB_CLIENT_TOKEN"),
    "APP_ID": os.getenv("VERIHUB_APP_ID"),
    "API_KEY": os.getenv("VERIHUB_API_KEY"),
    "KTP_SYNC": os.getenv("VERIHUB_URL_KTP_SYNC"),
    "COMPARE_PHOTO": os.getenv("VERIHUB_URL_COMPARE_PHOTO"),
    "DATA_VERIFICATION": os.getenv("VERIHUB_URL_DATA_VERIFICATION"),
}


XENDIT = {
    "CLIENT_URL": os.getenv("XENDIT_CLIENT_URL"),
    "CLIENT_SECRET_KEY": os.getenv("XENDIT_CLIENT_SECRET_KEY"),
    "CLIENT_PUBLIC_KEY": os.getenv("XENDIT_CLIENT_PUBLIC_KEY"),
    "WEBHOOK_KEY": os.getenv("XENDIT_WEBHOOK_KEY"),
    "API_VERSION": os.getenv("XENDIT_API_VERSION"),
}


# Email configuration
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "")
DEFAULT_FROM_EMAIL = os.getenv("EMAIL_HOST_USER", "")
EMAIL_SITE_URL = os.getenv("EMAIL_SITE_URL", "http://localhost:8000")
