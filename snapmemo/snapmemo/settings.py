"""
Django settings for snapmemo project.
using Django 1.11.6.
"""
import json
import os

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('MODE') == 'DEBUG'

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT_DIR = os.path.dirname(BASE_DIR)

# config directory setting
conf_dir = os.path.join(os.path.dirname(BASE_DIR), '.conf-secret')
# common config file setting
if DEBUG:
    COMMON_CONF_FILE = json.loads(open(os.path.join(conf_dir, 'config-common.json')).read())
else:
    COMMON_CONF_FILE = json.loads(open(os.path.join(conf_dir, 'config-deploy.json')).read())
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = COMMON_CONF_FILE['django']['secret-key']

ALLOWED_HOSTS = COMMON_CONF_FILE['django']['allowed-host']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_auth',
    'storages',
    'user',
    'memo'
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    )
}

# Send Email Settings
EMAIL_BACKEND = COMMON_CONF_FILE['django']['email']['EMAIL_BACKEND']
EMAIL_HOST = COMMON_CONF_FILE['django']['email']['EMAIL_HOST']
EMAIL_HOST_USER = COMMON_CONF_FILE['django']['email']['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = COMMON_CONF_FILE['django']['email']['EMAIL_HOST_PASSWORD']
EMAIL_PORT = COMMON_CONF_FILE['django']['email']['EMAIL_PORT']
EMAIL_USE_TLS = COMMON_CONF_FILE['django']['email']['EMAIL_USE_TLS']
DEFAULT_FROM_EMAIL = COMMON_CONF_FILE['django']['email']['DEFAULT_FROM_EMAIL']

# S3 Settings
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_ACCESS_KEY_ID = COMMON_CONF_FILE['aws']['access-key-id']
AWS_SECRET_ACCESS_KEY = COMMON_CONF_FILE['aws']['secret-access-key']
AWS_STORAGE_BUCKET_NAME = 'pemo'
MEDIAFILES_LOCATION = 'MEDIA_S3_DIR'
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
AWS_LOCATION = 'static'

MEDIA_URL = 'https://%s/MEDIA_DIR/' % AWS_S3_CUSTOM_DOMAIN

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'snapmemo/static'),
]
STATIC_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Media Settings
MEDIA_ROOT = os.path.join(BASE_DIR, 'upload')

ROOT_URLCONF = 'snapmemo.urls'

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

WSGI_APPLICATION = 'snapmemo.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': COMMON_CONF_FILE['django']['db']['ENGINE'],
        'NAME': COMMON_CONF_FILE['django']['db']['NAME'],
        'USER': COMMON_CONF_FILE['django']['db']['USER'],
        'PASSWORD': COMMON_CONF_FILE['django']['db']['PASSWORD'],
        'HOST': COMMON_CONF_FILE['django']['db']['HOST'],
        'PORT': COMMON_CONF_FILE['django']['db']['PORT']
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators
AUTH_USER_MODEL = 'user.Member'
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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'ko-kr'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
