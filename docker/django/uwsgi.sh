#!/usr/bin/env sh

set -o errexit
set -o nounset

# We are using `uwsgi` for production, see:
# http://docs.gunicorn.org/en/stable/configure.html

# Check that $DJANGO_ENV is set to "production",
# fail otherwise, since it may break things:
echo "DJANGO_ENV is $DJANGO_ENV"
if [[ "$DJANGO_ENV" != 'production' ]]; then
  echo 'Error: DJANGO_ENV is not set to "production".'
  echo 'Application will not start.'
  exit 1
fi

export DJANGO_ENV

# Run python specific scripts:
# Running migrations in startup script might not be the best option, see:
# docs/pages/template/production-checklist.rst
python manage.py migrate --noinput
python manage.py collectstatic --noinput
python manage.py compilemessages

# Start uwsgi:
/usr/local/bin/uwsgi --http :8000 \
    --chdir=/usr/src/app \
    --module=config.wsgi:application \
    --master \
    --workers=4 \
    --enable-threads \
    --max-requests=2000 \
    --stats :8001 \
    --stats-http \
    --memory-report
