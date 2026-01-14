#!/usr/bin/env bash

set -o errexit
set -o nounset
set -o pipefail

# Initializing global variables and functions:
: "${DJANGO_ENV:=development}"

# Fail CI if `DJANGO_ENV` is not set to `development`:
if [ "$DJANGO_ENV" != 'development' ]; then
  echo 'DJANGO_ENV is not set to development. Running tests is not safe.'
  exit 1
fi

pyclean () {
  # Cleaning cache:
  find . \
    | grep -E '(__pycache__|\.(mypy_|pytest_)?cache|(\/)?\.(hypothesis|perm|static)|\.py[cod]$)' \
    | xargs rm -rf \
  || true
}

run_ci () {
  echo '[ci started]'
  set -x  # we want to print commands during the CI process.

  # Testing filesystem and permissions:
  touch .perm && rm -f .perm
  touch '/usr/share/nginx/django/static/.perm' && rm -f '/usr/share/nginx/django/static/.perm'
  touch '/usr/share/nginx/django/media/.perm' && rm -f '/usr/share/nginx/django/media/.perm'

  # Checking `.env` files:
  dotenv-linter .env .env.template

  # Running linting for all python files in the project:
  pre-commit run --all-files

  # Running type checking, see https://github.com/typeddjango/django-stubs
#  mypy manage.py server $(find tests -name '*.py')

  # Running tests:
#  pytest --dead-fixtures
#  pytest

  # Run checks to be sure we follow all django's best practices:
  python manage.py check --fail-level WARNING

  # Run checks to be sure settings are correct (production flag is required):
  DJANGO_ENV=production python manage.py check --deploy --fail-level WARNING

  # Check that staticfiles app is working fine:
  DJANGO_ENV=production DJANGO_COLLECTSTATIC_DRYRUN=1 \
    python manage.py collectstatic --no-input --dry-run

  # Check that all migrations worked fine:
  python manage.py makemigrations --dry-run --check

  # Check that all migrations are backwards compatible:
  python manage.py lintmigrations --warnings-as-errors

  # Checking if all the dependencies are secure and do not have any
  # known vulnerabilities:
  safety check --full-report || true

  # Checking `pyproject.toml` file contents:
#  poetry check

  # Checking dependencies status:
  pip check

  # Checking docs:
#  doc8 -q docs

  # Checking `yaml` files:
  yamllint -d '{"extends": "default", "rules": {line-length: {max: 120}}, "ignore": "env"}' -s .

  # Checking translation files, ignoring ordering and locations:
  polint -i location,unsorted locale apps

#  # Also checking translation files for syntax errors:
#  if find locale -name '*.po' -print0 | grep -q "."; then
#    # Only executes when there is at least one `.po` file:
#    dennis-cmd lint --errorsonly locale
#  fi

  set +x
  echo '[ci finished]'
}

# Remove any cache before the script:
pyclean

# Clean everything up:
trap pyclean EXIT INT TERM

# Run the CI process:
run_ci
