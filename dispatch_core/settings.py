"""
Django settings for the DispatchDjango project.
Provides configuration for database, security, and application modules.
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-your-secret-key-here'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = []

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'dispatch_app',
]

# Custom User Model definition
AUTH_USER_MODEL = 'dispatch_app.CustomUser'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'dispatch_core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'dispatch_core.wsgi.application'

# Database configuration
# The project has been configured to use MariaDB
# instead of the default SQLite.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'dispatch_db',
        'USER': 'dispatch_admin',
        'PASSWORD': '***********',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'UserAttributeSimilarityValidator'
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'MinimumLengthValidator'
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'CommonPasswordValidator'
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'NumericPasswordValidator'
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'

# Static files configuration for global static folder.
# This helps PyCharm resolve the 'css/style.css' reference.
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Authentication Redirects
# Users will be sent to the home page after login or logout.
LOGIN_REDIRECT_URL = 'article_list'
LOGOUT_REDIRECT_URL = 'home'
# This ensures Django knows where the custom login page is located.
LOGIN_URL = 'login'

# Email Configuration for Development
# Emails will be printed to the standard output (console).
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = 'noreply@dispatch-django.com'

# X (formerly Twitter) Application Programming Interface configuration.
# These credentials are required for the automated posting feature.
# Replace the placeholder strings with your actual keys from the X
# Developer Portal.
# noinspection SpellCheckingInspection
X_API_KEY = 'your-api-key-here'
# noinspection SpellCheckingInspection
X_API_SECRET_KEY = 'your-api-secret-here'

# New tokens for automated posting
# noinspection SpellCheckingInspection
X_ACCESS_TOKEN = 'your-access-token-here'
# noinspection SpellCheckingInspection
X_ACCESS_TOKEN_SECRET = 'your-access-token-secret-here'
# noinspection SpellCheckingInspection
X_BEARER_TOKEN = 'your-bearer-token-here'
