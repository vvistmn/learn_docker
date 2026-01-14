from datetime import timedelta

from config.settings.components import env

CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"

CELERY_BROKER_URL = env.str("CELERY_BROKER_URL")
"""Адрес подключения к бекенду для публикации сообщений"""
CELERY_BROKER_CONNECTION_TIMEOUT = 10
"""Время подключения к брокеру сообщений (не работает для отправки сообщений)"""
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True
"""Пытаться подключиться к брокеру при запуске Celery"""
CELERY_BROKER_CONNECTION_MAX_RETRIES = 5
"""Количество попыток подключения к брокеру сообщений"""
CELERY_BROKER_TRANSPORT_OPTIONS = env.dict(var="CELERY_BROKER_TRANSPORT_OPTIONS",
                                           default={"visibility_timeout": env.int(var="CELERY_TASK_TIME_LIMIT",
                                                                                  default=60 * 5) + 60},
                                           cast={"cast": {"visibility_timeout": int}})
# visibility_timeout
# Время за которое воркер должен подтвердить сообщение. По истечении сообщение будет передано другому воркеру

# ----------
# Хранение результатов выполнения задач
# ----------
CELERY_RESULT_BACKEND = env.str("CELERY_RESULT_BACKEND", default="django-db")
"""Тип бекэнда для хранения результатов выполнения задач"""
CELERY_RESULT_EXTENDED = True
"""Включение хранения расширенных атрибутов результатов выполнения задач"""
CELERY_RESULT_EXPIRES = timedelta(days=env.int("CELERY_RESULT_EXPIRES", default=7))
"""Срок хранения результата выполнения задач"""
if CELERY_RESULT_EXPIRES > timedelta(days=7):
    raise Exception(f"Too long period for CELERY_RESULT_EXPIRES. Max: 7 days. Current: {CELERY_RESULT_EXPIRES}")


# ----------
# Параметры работы воркеров
# ----------
CELERY_WORKER_CONCURRENCY = 1
"""Количество одновременных рабочих процессов/потоков выполняющих задачи"""
CELERY_WORKER_DEDUPLICATE_SUCCESSFUL_TASKS = env.bool("CELERY_WORKER_DEDUPLICATE_SUCCESSFUL_TASKS", default=True)
"""Перед каждым выполнением задачи попросите работника проверить, не является ли эта задача дублирующим сообщением"""
CELERY_WORKER_PREFETCH_MULTIPLIER = 1
"""Количество сообщение для предварительной выборки за раз. 1 - для отключение предварительной выборки"""
CELERY_WORKER_SEND_TASK_EVENTS = True
"""Отправка событий связанных с задачами для отслеживания состояния во Flower"""
# CELERY_WORKER_MAX_MEMORY_PER_CHILD = 384000
"""Максимальный объем памяти для каждого воркера в КБ. Не работает в SOLO-режиме"""
CELERY_WORKER_PROC_ALIVE_TIMEOUT = env.int("CELERY_WORKER_PROC_ALIVE_TIMEOUT", default=10)
"""Таймаут в секунда при ожидании запуска нового воркера"""

# ----------
# Параметры сообщений
# ----------
CELERY_TASK_ACKS_LATE = True
"""Подтверждение сообщения после его выполнения. (Помогает ограничить количество задач бронируемых воркером)"""
CELERY_TASK_ALWAYS_EAGER = env.bool("CELERY_TASK_ALWAYS_EAGER", default=False)
"""Отключение фонового выполнения задач. (Для тестов)"""
CELERY_TASK_STORE_EAGER_RESULT = env.bool("CELERY_TASK_STORE_EAGER_RESULT", default=True)
"""Сохранение результатов """
CELERY_TASK_SOFT_TIME_LIMIT = env.int("CELERY_TASK_SOFT_TIME_LIMIT", default=None)
"""Мягкое максимальное время выполнения задачи. Воркер не умирает, но задача падает с ошибкой"""
CELERY_TASK_TIME_LIMIT = env.int("CELERY_TASK_TIME_LIMIT", default=None)
"""Максимальное время выполнения задачи. Воркер умирает. Задача падает с ошибкой. on_failure не отрабатывает"""
if CELERY_TASK_SOFT_TIME_LIMIT and CELERY_TASK_TIME_LIMIT and CELERY_TASK_SOFT_TIME_LIMIT >= CELERY_TASK_TIME_LIMIT:
    raise Exception("Variable CELERY_TASK_SOFT_TIME_LIMIT can't be less than CELERY_TASK_TIME_LIMIT")

CELERY_TASK_TRACK_STARTED = env.bool("CELERY_TASK_TRACK_STARTED", default=True)
"""Записывать начало выполнения задачи"""
CELERY_TASK_REJECT_ON_WORKER_LOST = env.bool("CELERY_TASK_REJECT_ON_WORKER_LOST", default=True)
"""Возвращать сообщение обратно в очередь если воркер умер или превышено время выполнения задачи(лучше не надо)"""
# CELERY_TASK_ROUTES = {
#
# }
# """Настройка маршрутизации Celery-задач и очередей"""
