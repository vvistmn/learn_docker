from logging import getLogger

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT

from apps.api.v1.auth.serializers import GroupSerializer, UserSerializer

UserModel = get_user_model()

logger = getLogger()


class UserViewSet(viewsets.ModelViewSet):
    """
    Конечная точка API, которая позволяет просматривать или редактировать пользователей.

    list:
    Получить список пользователей

    create:
    Создать нового пользователя

    flush:
    Очистка списка пользователей кроме `superuser`
    """

    queryset = UserModel.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    lookup_field = "username"

    @action(
        methods=["DELETE"],
        detail=False,
        name="flush",
        description="Очистка всех пользователей кроме `superuser`")
    def flush(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            raise PermissionDenied
        self.get_queryset().exclude(is_superuser=True).delete()
        return Response(status=HTTP_204_NO_CONTENT)


class GroupViewSet(viewsets.ModelViewSet):
    """Конечная точка API, которая позволяет просматривать или редактировать группы пользователей."""

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def list(self, request, *args, **kwargs):  # noqa: A003
        return super().list(request, *args, **kwargs)
