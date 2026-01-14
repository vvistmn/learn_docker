from django.urls import include, path

urlpatterns = [
    path(r"auth/", include("apps.api.v1.auth.urls"))
]
