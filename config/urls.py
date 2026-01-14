"""Django_blog URL Configuration."""

from django.conf import settings
from django.contrib import admin
from django.contrib.admindocs import urls as admindocs_urls
from django.contrib.auth import views as auth_views
from django.urls import include, path, re_path
from django.views.generic import RedirectView, TemplateView

from config.compat import is_applied
from config.settings.components.rest_framework import SchemaView

url_patterns_admin = [
    # Документация
    path("admin/doc/", include(admindocs_urls)),
    # Восстановление пароля
    path("admin/password_reset/", auth_views.PasswordResetView.as_view(), name="admin_password_reset"),
    path("admin/password_reset/done/", auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
    # Панель администратора. Добавляется ОБЯЗАТЕЛЬНО после других префиксов admin/ иначе не будет работать
    path("admin/", admin.site.urls),
    # Text and xml static files:
    path("robots.txt", TemplateView.as_view(
        template_name="txt/robots.txt",
        content_type="text/plain",
    )),
    path("humans.txt", TemplateView.as_view(
        template_name="txt/humans.txt",
        content_type="text/plain",
    )),
]

urlpatterns_api = [
    # API
    path(r"api/", include("apps.api.urls")),
    path(r"api-auth/", include("rest_framework.urls", namespace="rest_framework")),
]

if is_applied("drf_yasg"):
    urlpatterns_api += [
        re_path(r"^swagger(?P<format>\.json|\.yaml)$", SchemaView.without_ui(cache_timeout=0), name="schema-json"),
        re_path(r"^swagger/$", SchemaView.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
        re_path(r"^redoc/$", SchemaView.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
        re_path(r"^$", RedirectView.as_view(url=settings.URL_PREFIX + "/swagger/"))
    ]


urlpatterns_django = [
    # Адреса для django-приложений если не использовать API
]

urlpatterns_ = url_patterns_admin + urlpatterns_api + urlpatterns_django

if is_applied("schema_graph"):
    from schema_graph.views import Schema

    urlpatterns_ += [path("graph/", Schema.as_view())]

if is_applied("health_check"):
    urlpatterns_ += [path("health/", include("health_check.urls"))]

if settings.DEBUG and is_applied("debug_toolbar"):
    import debug_toolbar

    urlpatterns_ = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns_

if settings.URL_PREFIX:
    prefix = settings.URL_PREFIX.lstrip("/")
    urlpatterns = [path(prefix + "/", include(urlpatterns_))]
    settings.MEDIA_URL = "/" + prefix + settings.MEDIA_URL
    settings.STATIC_URL = "/" + prefix + settings.STATIC_URL
else:
    urlpatterns = [path("", include(urlpatterns_))]

if settings.DEBUG:
    from django.conf.urls.static import static

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
