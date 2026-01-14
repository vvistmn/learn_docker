from django.utils.translation import gettext_lazy as _

from config.settings.components import ROOT_DIR, env

SECRET_KEY = env.str("DJANGO_SECRET_KEY")

# --------------------
# APPLICATIONS
# --------------------
DJANGO_APPS = [
    # Default django apps
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Django-admin
    "django.contrib.admin",
    "django.contrib.admindocs",
]

THIRD_PARTY_APPS = [
    "django_extensions",
    # django apps
    "health_check",
    "health_check.db",
    "health_check.cache",
    "health_check.storage",
    "health_check.contrib.redis",
]

LOCAL_APPS = [

]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# --------------------
# DATABASES
# --------------------
_DJANGO_DATABASE_DEFAULT_OPTIONS = {
    # Время установки подключения
    "connect_timeout": 10,
    # Дополнительные параметры: максимальное время выполнения запроса
    "options": "-c statement_timeout=15000ms",
    # Имя приложения которое подключается
    "application_name": "vi-learn-docker"
}
_DJANGO_DATABASE_OPTIONS = env.dict("DJANGO_DATABASE_OPTIONS", default=dict())

_DJANGO_DATABASE_DEFAULT_OPTIONS.update(_DJANGO_DATABASE_OPTIONS)

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env.str("POSTGRES_DB"),
        "USER": env.str("POSTGRES_USER"),
        "PASSWORD": env.str("POSTGRES_PASSWORD"),
        "HOST": env.str("DJANGO_DATABASE_HOST"),
        "PORT": env.int("DJANGO_DATABASE_PORT"),
        "CONN_MAX_AGE": env.int("DJANGO_DATABASE_CONN_MAX_AGE", default=60),
        "OPTIONS": _DJANGO_DATABASE_DEFAULT_OPTIONS,
        "TEST": {
            "NAME": env.str("POSTGRES_TEST_DB", default=env.str("POSTGRES_DB") + "-test"),
        }
    },
}

# --------------------
# MIDDLEWARE
# --------------------

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    # Управление сессиями между запросами
    "django.contrib.sessions.middleware.SessionMiddleware",
    # Управление локализацией приложения
    "django.middleware.locale.LocaleMiddleware",
    # Запрет user-agent, нормализация url, назначение длины запроса
    "django.middleware.common.CommonMiddleware",
    # Проверка csrf-токенов для встроенных форм Django
    "django.middleware.csrf.CsrfViewMiddleware",
    # Связывание пользователей с запросами используя сессии
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# --------------------
# TEMPLATES
# --------------------

TEMPLATES = [
    {
        "APP_DIRS": True,
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            ROOT_DIR.path("config", "templates").root,
        ],
        "OPTIONS": {
            "context_processors": [
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.debug",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.request",
            ],
        },
    },
]

# --------------------
# COMMON
# --------------------
WSGI_APPLICATION = "config.wsgi.application"

LANGUAGE_CODE = "ru-ru"

USE_I18N = True
USE_L10N = True

LANGUAGES = (
    ("ru", _("Russian")),
    ("en", _("English"))
)

LOCALE_PATHS = (
    ROOT_DIR.path("locale"),
)

USE_TZ = True
TIME_ZONE = "UTC"

# --------------------
# URLS
# --------------------
ROOT_URLCONF = "config.urls"

URL_PREFIX = env.str("DJANGO_URL_PREFIX", default="")

LOGIN_URL = "rest_framework:login"
LOGOUT_URL = "rest_framework:logout"

LOGIN_REDIRECT_URL = URL_PREFIX + "/"

# --------------------
# STATIC
# --------------------
STATIC_URL = "/static/"

STATIC_ROOT = ROOT_DIR.path("static")

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
)

# --------------------
# MEDIA
# --------------------
MEDIA_URL = "/media/"

MEDIA_ROOT = ROOT_DIR.path("media")

APPEND_SLASH = True

# --------------------
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher"
]

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"
