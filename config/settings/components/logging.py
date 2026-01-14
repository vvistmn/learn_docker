# --------------------
# LOGGING
# https://docs.djangoproject.com/en/2.2/topics/logging/
from config.settings.components import env

CELERY_LOG_LEVEL = env("CELERY_LOG_LEVEL", default="INFO")
CELERY_TASK_LOG_LEVEL = env("CELERY_TASK_LOG_LEVEL", default="INFO")
DJANGO_LOG_LEVEL = env.str("DJANGO_LOG_LEVEL", "INFO")

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(asctime)s [%(levelname)s] %(thread)d [%(process)d]  %(filename)s:%(lineno)s %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "simple": {
            "format": "%(asctime)s [%(levelname)s] [%(name)s] %(threadName)s %(filename)s:[%(lineno)s] %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "filters": {
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue"
        }
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "filters": ["require_debug_true"],
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
        "console-verbose": {
            "level": "DEBUG",
            "filters": ["require_debug_true"],
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
        "celery": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "propagate": True,
            "level": DJANGO_LOG_LEVEL,
        },
        "security": {
            "handlers": ["console-verbose"],
            "level": "ERROR",
            "propagate": False,
        },
        "celery_tasks": {
            "handlers": ["celery"],
            "propagate": False,
            "level": CELERY_TASK_LOG_LEVEL
        },
        "celery": {
            "handlers": ["celery"],
            "propagate": False,
            "level": CELERY_LOG_LEVEL
        },

    },
    "root": {
        "level": DJANGO_LOG_LEVEL,
        "handlers": ["console"]
    }
}
# --------------------
