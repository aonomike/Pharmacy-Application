"""
Django settings for ARVDispenser project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'q%8lw&i-!ir98)_ervkr%j-^)343_eh!afx4%-(hza$-qdo%mn'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Internal Django applications here
DJANGO_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',

    )
# Third-party applications here
THIRD_PARTY_APPS = (
    'south',
    )

#Local applications here
LOCAL_APPS = (
    'patients',
    'ARTRegimen',
    'commodities',
    'sourceOrDestination',
    'transactions',
    'visits',
    'user_account',
    'AuditTrail',
    )

# Application definition
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'ARVDispenser.urls'

WSGI_APPLICATION = 'ARVDispenser.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'arvdispenser',
        'USER': 'root',
        'PASSWORD':'',
        'HOST':'',
        'PORT':'3306',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'



USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

#local directory that stores static files(css,js,imgs)
STATIC_ROOT =os.path.join(BASE_DIR,'served')

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),

    )

TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )),
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s \n',
            'datefmt' : "%d %b %Y %H:%M:%S"
        },
    },
    'handlers': {
        'default': {
            'level': 'INFO',
            'class':'logging.handlers.RotatingFileHandler',
            'filename':'logs/mylog.log',
            'maxBytes':1024*1024*5,
            'backupCount':5,
            'formatter':'standard',
        },
    
    'request_handler': {
            'level': 'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename':'logs/django_request.log',
            'maxBytes':1024*1024*5,
            'backupCount':5,
            'formatter':'standard',
        },
    },
    'loggers':{
    '':{
        'handlers':['default'],
        'level':'INFO',
        'propagate':True
        },
    'django.request':{
        'handlers':['request_handler'],
        'level':'DEBUG',
        'propagate':False
        },

    }
}
