from config import compat
from config.settings.components import env
from config.settings.components.common import DATABASES, INSTALLED_APPS, MIDDLEWARE

DEBUG = True

ALLOWED_HOSTS = [env.str("DOMAIN_NAME", default="localhost"),
                 "localhost",
                 "0.0.0.0",
                 "127.0.0.1",
                 "[::1]",
                 ] + env.list("DJANGO_ALLOWED_HOSTS", default=[])

STATICFILES_DIRS = []

# --------------------
# DJANGO-SCHEMA-GRAPH
# --------------------
if compat.is_installed("schema_graph"):
    INSTALLED_APPS.append("schema_graph")

# --------------------
# DEBUG_TOOLBAR
# --------------------
if compat.is_installed("debug_toolbar"):
    INSTALLED_APPS.append("debug_toolbar")

    MIDDLEWARE.append("debug_toolbar.middleware.DebugToolbarMiddleware")


def custom_show_toolbar(request):
    """Only show the debug toolbar to users with the superuser flag."""
    return request.user.is_superuser


DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK":
        "config.settings.environments.development.custom_show_toolbar",
}

# --------------------
# QUERYCOUNT
# --------------------
if compat.is_installed("querycount"):
    MIDDLEWARE.append("querycount.middleware.QueryCountMiddleware")

QUERYCOUNT = {
    "THRESHOLDS": {
        "MEDIUM": 50,
        "HIGH": 200,
        "MIN_TIME_TO_LOG": 0.5,
        "MIN_QUERY_COUNT_TO_LOG": 2
    },
    "IGNORE_REQUEST_PATTERNS": [r"^/admin/"],
    "IGNORE_SQL_PATTERNS": [r"silk_"],
    "DISPLAY_DUPLICATES": None,
    "RESPONSE_HEADER": "X-DjangoQueryCount-Count"
}

# -------------------
# DJANGO-TEST-MIGRATION
# https://github.com/wemake-services/django-test-migrations
# -------------------
if compat.is_installed("django_test_migrations"):
    INSTALLED_APPS.append("django_test_migrations.contrib.django_checks.DatabaseConfiguration")

# -------------------
# DJANGO-MIGRATION-LINTER
#   https://github.com/3YOURMIND/django-migration-linter
# -------------------
if compat.is_installed("django_migration_linter"):
    INSTALLED_APPS.append("django_migration_linter")

# -------------------
# DJANGO-EXTRA-CHECK
# https://github.com/kalekseev/django-extra-checks
# -------------------
if compat.is_installed("extra_checks"):
    INSTALLED_APPS.append("extra_checks")

EXTRA_CHECKS = {
    "checks": [
        # Forbid `unique_together`:
        "no-unique-together",
        # Require non empty `upload_to` argument:
        "field-file-upload-to",
        # Use the indexes option instead:
        "no-index-together",
        # Each model must be registered in admin:
        "model-admin",
        # FileField/ImageField must have non empty `upload_to` argument:
        "field-file-upload-to",
        # Text fields shouldn"t use `null=True`:
        "field-text-null",
        # Prefer using BooleanField(null=True) instead of NullBooleanField:
        "field-boolean-null",
        # Don"t pass `null=False` to model fields (this is django default)
        "field-null",
        # ForeignKey fields must specify db_index explicitly if used in other indexes:
        {"id": "field-foreign-key-db-index", "when": "indexes"},
        # If field nullable `(null=True) then default=None argument is redundant and should be removed:
        "field-default-null",
        # Fields with choices must have companion CheckConstraint to enforce choices on database level
        "field-choices-constraint",
        # All model's fields must have verbose name.
        "field-verbose-name",
        # Verbose_name must use gettext.
        "field-verbose-name-gettext"
    ]
}

DATABASES["default"]["CONN_MAX_AGE"] = 0
