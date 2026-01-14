from contextlib import suppress
import environ

env = environ.Env()

ROOT_DIR = environ.Path(__file__) - 4  # __init__.py/components/settings/config/<service>
APPS_DIR = ROOT_DIR.path("apps")

env_file = env.ENVIRON.get("DOT_ENV_FILE")
if not env_file:
    env_file = str(ROOT_DIR.path(".env"))

# https://docs.python.org/3/library/contextlib.html#contextlib.suppress
with suppress(FileNotFoundError), open(env_file, encoding="utf-8") as f:
    env.read_env(f)
