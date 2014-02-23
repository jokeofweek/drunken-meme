"""
Django settings for smapchat project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import pprint
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '^bq#_$6vpi-#11v6zclvelu^t37y264#9&b^#g*t46y_=n#k7$'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bootstrap3',
    'allaccess',
    'south',
    'django_extensions',
    'smapchat'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

AUTHENTICATION_BACKENDS = (
    # Default backend
    'django.contrib.auth.backends.ModelBackend',
    # Additional backend
    'allaccess.backends.AuthorizedServiceBackend',
)

ROOT_URLCONF = 'smapchat.urls'

WSGI_APPLICATION = 'smapchat.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
import json
with open(BASE_DIR + "/../settings.json") as filename:
	env = json.load(filename)
DATABASES = {
    'default': env
}


# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, '/smapchat/templates/static/')
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

#STATIC_ROOT = '/smapchat/templates/static/'
#STATIC_ROOT = '/home/ec2-user/sds/static/'


TEMPLATE_DIRS = (
    BASE_DIR + '/smapchat/templates/',
)
