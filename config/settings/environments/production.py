from environ import Path

from config.compat import is_installed
from config.settings.components import env

DEBUG = False

ALLOWED_HOSTS = [
    "localhost",
    env.str("DOMAIN_NAME", default="localhost")
] + env.list("DJANGO_ALLOWED_HOSTS", default=[])

_COLLECTSTATIC_DRYRUN = env.bool("DJANGO_COLLECTSTATIC_DRYRUN", default=False)

STATIC_ROOT = Path(".static") if _COLLECTSTATIC_DRYRUN else env.path("DJANGO_STATIC_ROOT", default=Path("/usr/share/nginx/django/static"))  # noqa: E501

MEDIA_ROOT = env.path("DJANGO_MEDIA_ROOT", default=Path("/usr/share/nginx/django/media"))


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# --------------------
# SENTRY.IO
# --------------------
if is_installed("sentry_sdk"):
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration

    sentry_sdk.init(
        dsn=env.str("SENTRY_DSN", default=""),
        integrations=[DjangoIntegration()]
    )

SECURE_HSTS_SECONDS = 31536000  # the same as Nginx has
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = True
SECURE_REDIRECT_EXEMPT = [
    # This is required for healthcheck to work:
    "^health/",
]

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
