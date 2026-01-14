"""
Django REST framework is a powerful and flexible toolkit for building Web APIs.

https://github.com/encode/django-rest-framework

* Python: 3.5, 3.6, 3.7, 3.8, 3.9
* Django: 2.2, 3.0, 3.1

"""
from config.compat import is_installed
from config.settings.components.common import INSTALLED_APPS

# --------------------
# DJANGO-REST-FRAMEWORK
# --------------------
if is_installed("rest_framework"):
    INSTALLED_APPS += [
        # Rest API
        "rest_framework",
    ]

REST_FRAMEWORK = {
    # Классы используемые для аутентификации
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.BasicAuthentication",
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework_simplejwt.authentication.JWTAuthentication"
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated"
    ],
    # Классы используемые для рендера ответа
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
    ],
    # Класс по умолчанию для пагинации
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 10,
    # Фильтрация
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend"
    ]
}

REST_FRAMEWORK_EXTENSIONS = {
    "DEFAULT_PARENT_LOOKUP_KWARG_NAME_PREFIX": ""
}

SchemaView = None
if is_installed("drf_yasg"):
    from drf_yasg import openapi  # noqa: E402
    from drf_yasg.views import get_schema_view

    INSTALLED_APPS.append("drf_yasg")
    SchemaView = get_schema_view(
        openapi.Info(
            title="Snippets API",
            default_version="v1",
            description="Test description",
            terms_of_service="https://www.google.com/policies/terms/",
            contact=openapi.Contact(email="contact@snippets.local"),
            license=openapi.License(name="BSD License"),
        ),
        public=True,
    )
