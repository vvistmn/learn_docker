from split_settings.tools import include, optional

from config.settings.components import env

ENV = env.str("DJANGO_ENV", default="development")

base_settings = [
    # Базовые компоненты
    "components/common.py",
    "components/smtp.py",
    "components/caches.py",
    "components/logging.py",
    "components/security.py",
    "components/rest_framework.py",
    "components/corsheaders.py",
    "components/celery.py",
    "components/redis.py",
    # Разрабатываемые приложения

    # Режим запуска (development, production, test, any...)
    f"environments/{ENV}.py",

    # Опциональные зависимости
    optional("local.py")
]

# Сбор всех настроек вместе
include(*base_settings)
