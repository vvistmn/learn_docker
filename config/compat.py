"""Модуль для проверки установлены ли те или иные библиотеки."""
from importlib import import_module

from django.conf import settings


def is_installed(package: str) -> bool:
    """Проверка установки какого-либо пакета."""
    try:
        module = import_module(package)
    except ImportError:
        module = None
    return module is not None


def is_applied(app: str) -> bool:
    """
    Проверка установки пакета и добавления его в INSTALLED_APPS.

    :param app: имя приложения
    :return: флаг наличия приложения в INSTALLED_APPS
    :rtype: bool
    """
    return is_installed(app) and app in settings.INSTALLED_APPS
