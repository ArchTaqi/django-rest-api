import os, datetime

from configurations import Configuration, values


class Common(Configuration):
    # Build paths inside the project like this: os.path.join(BASE_DIR, ...)
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))

    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = values.SecretValue()

    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = values.BooleanValue(False)

    # Allow all host headers
    ALLOWED_HOSTS = values.ListValue([])
    SITE_ID = 1
    # Honor the 'X-Forwarded-Proto' header for request.is_secure()
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

    # Application definition
    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'whitenoise.runserver_nostatic',
        'django.contrib.staticfiles',

        'django_extensions',
        'debug_toolbar',
        'rest_framework',
        'rest_framework_swagger',
        'django_filters',

        'apps.users',
        'apps.pets',
    ]

    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'whitenoise.middleware.WhiteNoiseMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ]

    ROOT_URLCONF = 'django-rest-api.urls'

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [os.path.join(BASE_DIR, 'templates')],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                    'django.template.context_processors.i18n',
                    'django.template.context_processors.media',
                    'django.template.context_processors.static',
                    'django.template.context_processors.tz',
                ],
            },
        },
    ]

    WSGI_APPLICATION = 'django-rest-api.wsgi.application'

    # Database
    # https://docs.djangoproject.com/en/2.1/ref/settings/#databases
    DATABASES = values.DatabaseURLValue(
        'sqlite:///{}'.format(os.path.join(BASE_DIR, 'db.sqlite3'))
    )

    # Password validation
    # https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators
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
    # https://docs.djangoproject.com/en/2.1/topics/i18n/
    LANGUAGE_CODE = 'en-us'
    TIME_ZONE = 'UTC'
    USE_I18N = True
    USE_L10N = True
    USE_TZ = True

    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/2.1/howto/static-files/
    STATIC_URL = '/static/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    # Extra places for collectstatic to find static files.
    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, 'static'),
    ]
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

    AUTH_USER_MODEL = 'users.User'

    REST_FRAMEWORK = {
        'DEFAULT_PERMISSION_CLASSES': (
            'rest_framework.permissions.IsAuthenticatedOrReadOnly',
            'rest_framework.permissions.IsAuthenticated',
            'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
        ),
        'DEFAULT_AUTHENTICATION_CLASSES': (
            'rest_framework.authentication.BasicAuthentication',
            'rest_framework.authentication.SessionAuthentication',
            'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        ),
        'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',),
        # When you enable API versioning, the request.version attribute will contain a string
        # that corresponds to the version requested in the incoming client request.
        'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.URLPathVersioning',
    }

    # JWT settings
    JWT_AUTH = {
        'JWT_ENCODE_HANDLER':
        'rest_framework_jwt.utils.jwt_encode_handler',

        'JWT_DECODE_HANDLER':
        'rest_framework_jwt.utils.jwt_decode_handler',

        'JWT_PAYLOAD_HANDLER':
        'rest_framework_jwt.utils.jwt_payload_handler',

        'JWT_PAYLOAD_GET_USER_ID_HANDLER':
        'rest_framework_jwt.utils.jwt_get_user_id_from_payload_handler',

        'JWT_RESPONSE_PAYLOAD_HANDLER':
        'rest_framework_jwt.utils.jwt_response_payload_handler',

        'JWT_SECRET_KEY': SECRET_KEY or "235856!gsdgsd",
        'JWT_GET_USER_SECRET_KEY': None,
        'JWT_PUBLIC_KEY': None,
        'JWT_PRIVATE_KEY': None,
        'JWT_ALGORITHM': 'HS256',
        'JWT_VERIFY': True,
        'JWT_VERIFY_EXPIRATION': True,
        'JWT_LEEWAY': 0,
        'JWT_EXPIRATION_DELTA': datetime.timedelta(seconds=3600),
        'JWT_AUDIENCE': None,
        'JWT_ISSUER': None,
        #
        'JWT_ALLOW_REFRESH': True,
        'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=7),

        'JWT_AUTH_HEADER_PREFIX': 'Bearer', # Bearer <token>
        'JWT_AUTH_COOKIE': None,
    }

    UPLOAD_FILE_PATH = os.path.join(BASE_DIR, 'upload/')
    try:
        if not os.path.exists(UPLOAD_FILE_PATH):
            os.makedirs(UPLOAD_FILE_PATH)
    except FileExistsError as e:
        print(e)
    except Exception as e:
        print(e)


class Development(Common):
    """
    The in-development settings and the default configuration.
    """
    DEBUG = True

    ALLOWED_HOSTS = []

    INTERNAL_IPS = [
        '127.0.0.1'
    ]

    MIDDLEWARE = Common.MIDDLEWARE + [
        'debug_toolbar.middleware.DebugToolbarMiddleware'
    ]


class Staging(Common):
    """
    The in-staging settings.
    """
    # Security
    SESSION_COOKIE_SECURE = values.BooleanValue(True)
    SECURE_BROWSER_XSS_FILTER = values.BooleanValue(True)
    SECURE_CONTENT_TYPE_NOSNIFF = values.BooleanValue(True)
    SECURE_HSTS_INCLUDE_SUBDOMAINS = values.BooleanValue(True)
    SECURE_HSTS_SECONDS = values.IntegerValue(31536000)
    SECURE_REDIRECT_EXEMPT = values.ListValue([])
    SECURE_SSL_HOST = values.Value(None)
    SECURE_SSL_REDIRECT = values.BooleanValue(True)
    SECURE_PROXY_SSL_HEADER = values.TupleValue(
        ('HTTP_X_FORWARDED_PROTO', 'https')
    )


class Production(Staging):
    """
    The in-production settings.
    """
    pass
