"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 1.11.1.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/

other sources used:
    https://medium.com/@djstein/modern-django-part-1-project-refactor-and-meeting-the-django-settings-api-d2784efb606f
"""
import os
import environ
import dj_database_url

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

ROOT_DIR = environ.Path(__file__) - 3
APPS_DIR = ROOT_DIR.path('project')


# This section added from an update to standards in CookieCutter Django to ensure no errors are encountered at runserver/migrations
env = environ.Env()
READ_DOT_ENV_FILE = env.bool('DJANGO_READ_DOT_ENV_FILE', default=False)
if READ_DOT_ENV_FILE:
    env_file = str(ROOT_DIR.path('.env'))
    print('Loading : {}'.format(env_file))
    env.read_env(env_file)
    print('The .env file has been loaded. See base.py for more information')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
#DEBUG = env.bool('DJANGO_DEBUG', True)
DEBUG = True

#TODO figure out where this goes 
#TODO figure out how this works with environ?
SITE_ID = 1

SECRET_KEY = '^+duvk^m9q1$bs9__&j18idqcpe@(dgxd&%=iuh9di631m%fq$'


# Application definition

DJANGO_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',
)

THIRD_PARTY_APPS = (
    'crispy_forms',
    'django_bitly',
    'django_social_share',
    'rest_framework',
)

LOCAL_APPS = (
    'project.api',
    'project.apicc',
)

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

#THIRD_PARTY_MIDDLEWARE = [
#        'whitenoise.middleware.WhiteNoiseMiddleware',
#]
#
#MIDDLEWARE = DJANGO_MIDDLEWARE + THIRD_PARTY_MIDDLEWARE

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        #TODO rewrite to use environ syntax
#        'DIRS': [os.path.join(os.path.dirname(__file__), 'templates'),],
        'DIRS': [ROOT_DIR.path('templates'),],
#        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# Database setting moved to sub settings
# Imported these setting from devcenter.Heroku
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Update database configuration with $DATABASE_URL.
db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)
DATABASES['default']['TEST'] = {'NAME': DATABASES['default']['NAME']}

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = str(ROOT_DIR('staticfiles'))
STATICFILES_DIRS = (
    str(APPS_DIR.path('static')),
)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)
MEDIA_URL = '/media/'
MEDIA_ROOT = str(APPS_DIR('media'))
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')

# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/
#TODO review this addition
STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

# REST Framework settings
REST_FRAMEWORK = {
}

# CRISPI FORMS settings
# let crispy tell you what's wrong - https://django-crispy-forms.readthedocs.io/en/latest/crispy_tag_forms.html#make-crispy-forms-fail-loud
#CRISPY_FAIL_SILENTLY = not DEBUG
CRISPY_FAIL_SILENTLY = not DEBUG
CRISPY_TEMPLATE_PACK = 'bootstrap3'

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
# https://djangogirls.gitbooks.io/django-girls-tutorial-extensions/heroku/
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

