# Django settings for swarming_heads project.

import logging
import os

# Keep all references relative to this file
SITE_ROOT = os.path.realpath(os.path.dirname(__file__))

DEBUG = True

TEMPLATE_DEBUG = DEBUG

LOG_LEVEL = logging.DEBUG
LOG_FILE = 'swarming_heads.log'

EM_HOST = '127.0.0.1'
EM_PORT = 30001

EM_TIMEOUT = 10; #Number of seconds to wait for connection to EM before timeout

HOOKBOX_HOST = '127.0.0.1'
HOOKBOX_PORT = 8001

SECRET_KEY = '+i%4%7_9u(j*1)o*zroago98np-z1z81##$1^2*@eu01ckl183'

ROOT_URLCONF = 'swarming_heads.urls'

TIME_ZONE = 'Australia/Sydney'

LANGUAGE_CODE = 'en-us'

SITE_ID = 1

USE_I18N = False

USE_L10N = True

STATIC_ROOT = os.path.join(SITE_ROOT, 'static')

STATIC_URL = '/static/'    

MEDIA_ROOT = os.path.join(SITE_ROOT, 'media')

MEDIA_URL = '/media/'

ADMIN_MEDIA_PREFIX = '/static/admin/'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(SITE_ROOT, 'db/database.db'),
        'USER': '',                      
        'PASSWORD': '',                  
        'HOST': '',                      
        'PORT': '',                      
    }
}

STATICFILES_DIRS = (    MEDIA_ROOT,
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)


TEMPLATE_DIRS = (
    os.path.join(SITE_ROOT, 'templates')             
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.humanize',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'apps.swarmingHeads',
)

