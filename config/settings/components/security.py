# --------------------
# SECURITY
# --------------------
# https://docs.djangoproject.com/en/2.2/topics/security/
from config.settings.components import env

SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

SECURE_REDIRECT_EXEMPT = [
    # This is required for healthcheck to work:
    "^health/",
]

_URL_PREFIX = env.str("DJANGO_URL_PREFIX", default="").lstrip("/").strip()
if _URL_PREFIX:
    SECURE_REDIRECT_EXEMPT = [
        f"^{_URL_PREFIX}/health/",
    ]

SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True

X_FRAME_OPTIONS = "DENY"
