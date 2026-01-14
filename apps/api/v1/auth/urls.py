from rest_framework import routers

from apps.api.v1.auth.views import GroupViewSet, UserViewSet

router = routers.DefaultRouter()

router.register(r"users", UserViewSet)
router.register(r"groups", GroupViewSet)

urlpatterns = router.urls
