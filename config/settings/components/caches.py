# -------------------
# CACHING
# https://docs.djangoproject.com/en/3.2/topics/cache/
# -------------------
from config.settings.components import env

CACHE_MIDDLEWARE_SECONDS = env.int("DJANGO_CACHE_MIDDLEWARE_SECONDS", default=600)
"""Время жизни кеша"""
CACHE_MIDDLEWARE_KEY_PREFIX = env.str("CACHE_MIDDLEWARE_KEY_PREFIX", default="")
"""Префикс ключей кеша"""

CACHES = {
    # Кеш на час
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
    },

}
