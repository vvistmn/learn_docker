"""
A Django App that adds Cross-Origin Resource Sharing (CORS) headers to responses.

This allows in-browser requests to your Django application from other origins.

* Python: 3.5, 3.6, 3.7, 3.8
* Django: 1.11, 2.1, 2.2, 3.0

"""
# --------------------
# DJANGO-CORS-HEADERS
# --------------------
from config import compat
from config.settings.components import env
from config.settings.components.common import INSTALLED_APPS, MIDDLEWARE

if compat.is_installed("corsheaders"):
    INSTALLED_APPS.append("corsheaders")
    MIDDLEWARE.insert(0, "corsheaders.middleware.CorsMiddleware")

CORS_ALLOWED_ORIGINS = env.list("DJANGO_CORS_ALLOWED_ORIGINS", default=[])
CORS_ALLOWED_ORIGIN_REGEXES = env.list("DJANGO_CORS_ALLOWED_ORIGIN_REGEXES", default=[])
CORS_ALLOW_ALL_ORIGINS = env.bool("DJANGO_CORS_ORIGIN_ALLOW_ALL", default=False)
