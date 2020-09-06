"""
Django settings for SmallCompany project.

"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '60hlmlg6pd9um^uwy(43)fy_z3y0v=&4h&y@g9ix@tc&#o_h)_'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'analytics.apps.AnalyticsConfig',
    'upload.apps.UploadConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
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

ROOT_URLCONF = 'SmallCompany.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'SmallCompany.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'smallco',
        'USER': 'pacman',
        'PASSWORD': 'pacman',
        'HOST': '192.168.43.65',   # Or an IP Address that your DB is hosted on
        'PORT': '3306'
        },
    }

# LOGGING Dict
LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                    'format': '({asctime}) - {levelname}'
                              ' {name}: {lineno} {module} '
                              '{process:d} {thread:d} {message}',
                    'style': '{',
                },
            'simple': {
                    'format': '{levelname} {message}',
                    'style': '{',
                },
            },
        'handlers': {
            'file': {
                'level': 'DEBUG',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': os.path.join(BASE_DIR, 'logs/debugger.log'),
                'formatter': 'verbose',
                },
            'console': {
                'level': 'INFO',
                'class': 'logging.StreamHandler',
                'formatter': 'simple',
                },
            },
        'loggers': {
            'django': {
                'handlers': ['file'],
                'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
                'propagate': True,
                },
            },
        'root': {
            'handlers': ['console'],
            'level': 'INFO'
            }
    }

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Calcutta'

USE_I18N = True

USE_L10N = False

USE_TZ = False

DATETIME_INPUT_FORMAT = ['%d-%m-%Y %H:%M:%S']

STATIC_URL = '/static/'

LOGIN_REDIRECT_URL = '/index/'

LOGOUT_REDIRECT_URL = 'login'

MEDIA_URL = 'upload/static/upload/'
MEDIA_ROOT = os.path.join(BASE_DIR, MEDIA_URL)
