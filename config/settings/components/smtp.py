# noqa: A005
from config.settings.components import env

EMAIL_CONFIG = env.email("DJANGO_EMAIL_URL", default="dummymail://")
if EMAIL_CONFIG:
    vars().update(EMAIL_CONFIG)
    EMAIL_OPTIONS_CONFIG = EMAIL_CONFIG.get("OPTIONS")
    if EMAIL_OPTIONS_CONFIG:
        vars().update(EMAIL_OPTIONS_CONFIG)