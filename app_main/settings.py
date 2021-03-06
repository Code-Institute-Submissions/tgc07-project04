"""
Django settings for app_main project.

Generated by 'django-admin startproject' using Django 3.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
from pathlib import Path
from dotenv import load_dotenv
import os
import dj_database_url


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Load environment variables
load_dotenv(os.path.join(BASE_DIR, '.env'))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True if os.environ.get('DEBUG_MODE')=="True" else False


ALLOWED_HOSTS = ["127.0.0.1", "localhost", os.environ.get('DEBUG_URL')] if os.environ.get('DEBUG_MODE')=="True" else ["tgc07-project04.herokuapp.com"]


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.humanize',

    # 3rd party
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'crispy_forms',
    'rest_framework',
    'mathfilters',

    # My apps
    'home',
    'sales',
    'tasks',
    'teams',
]


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


ROOT_URLCONF = 'app_main.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
            os.path.join(BASE_DIR, 'templates', 'allauth')
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


WSGI_APPLICATION = 'app_main.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases
if os.environ.get('DEBUG_MODE')=="True":
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    DATABASES = {
        'default': dj_database_url.parse(os.environ.get('DATABASE_URL'))
    }


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators
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
# https://docs.djangoproject.com/en/3.1/topics/i18n/
LANGUAGE_CODE = 'en-gb'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/
STATIC_URL = '/static/'
STATICFILES_DIRS = [ os.path.join(BASE_DIR, 'static') ]
# whitenoise static files directory for heroku deployment
STATIC_ROOT = "" if os.environ.get('DEBUG_MODE')=="True" else os.path.join(BASE_DIR, 'staticfiles')


AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
)


# allauth
SITE_ID = 1
# Allows user to login/register via a username or email
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
# User must specify an email address
ACCOUNT_EMAIL_REQUIRED = True
# Whether the must verify their email address
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
# Asks user to enter their email twice
ACCOUNT_SIGNUP_EMAIL_ENTER_TWICE = True
# Minimal length of the username
ACCOUNT_USERNAME_MIN_LENGTH = 4
# Log in page URL
LOGIN_URL = '/users/login/'
# Logged in successfully, redirect to here
LOGIN_REDIRECT_URL = '/teams/memberships/user/'
# Log user in if confirm email after account sign-up in same browser session
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True


# emails
if os.environ.get('DEBUG_MODE')=="True":
    # If debug_mode, emails displayed in terminal
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    # If production, emails sent via SMTP
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_USE_TLS = True
    EMAIL_PORT = 587
    EMAIL_HOST = "smtp.gmail.com"
    EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
    EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
    DEFAULT_FROM_EMAIL = os.environ.get("EMAIL_HOST_USER")


# Crispy Forms
CRISPY_TEMPLATE_PACK = 'bootstrap4'


# Stripe
STRIPE_PUBLISHABLE_KEY = os.environ.get('STRIPE_PUBLISHABLE_KEY')
STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY')
STRIPE_WEBHOOK_SIGNING_SECRET = os.environ.get('STRIPE_WEBHOOK_DEBUG') if os.environ.get('DEBUG_MODE')=="True" else os.environ.get('STRIPE_WEBHOOK_SIGNING_SECRET')
