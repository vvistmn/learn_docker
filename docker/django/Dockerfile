# This Dockerfile uses multi-stage build to customize DEV and PROD images:
# https://docs.docker.com/develop/develop-images/multistage-build/
FROM python:3.12-slim-bookworm AS development_build

LABEL maintainer="verdant24@yandex.ru"
LABEL vendor="vi"

ARG DJANGO_ENV=development \
    UID=1000 \
    GID=1000

SHELL ["/bin/bash", "-eo", "pipefail", "-c"]

ENV \
    DJANGO_ENV=${DJANGO_ENV} \
    # pyhon
    PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    # pip
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    PIP_ROOT_USER_ACTION=ignore \
    # dockerize
    DOCKERIZE_VERSION=v0.6.1


RUN rm -f /etc/apt/apt.conf.d/docker-clean; echo 'Binary::apt::APT::Keep-Downloaded-Packages "true";' > /etc/apt/apt.conf.d/keep-cache

RUN --mount=type=cache,target=/var/lib/apt,sharing=locked \
    --mount=type=cache,target=/var/cache/apt,sharing=locked \
    apt-get update && apt-get upgrade -y \
    && apt-get install --no-install-recommends -y \
    bash \
    build-essential \
    curl \
    gettext \
    git \
    libpq-dev \
    # Installing `dockerize` utility:
    # https://github.com/jwilder/dockerize
    && curl -sSLO "https://github.com/jwilder/dockerize/releases/download/${DOCKERIZE_VERSION}/dockerize-linux-amd64-${DOCKERIZE_VERSION}.tar.gz" \
    && tar -C /usr/local/bin -xzvf "dockerize-linux-amd64-${DOCKERIZE_VERSION}.tar.gz" \
    && rm "dockerize-linux-amd64-${DOCKERIZE_VERSION}.tar.gz" && dockerize --version

WORKDIR /usr/src/app

RUN groupadd -g "${GID}" -r web \
  && useradd -d "/usr/src/app" -g web -l -r -u "${UID}" web \
  && chown web:web -R "/usr/src/app" \
  # Static and media files:
  && mkdir -p "/usr/share/nginx/django/static" "/usr/share/nginx/django/media" \
  && chown web:web "/usr/share/nginx/django/static" "/usr/share/nginx/django/media"

COPY requirements requirements

# hadolint ignore=SC2046
RUN --mount=type=cache,target="/root/.cache/pip",sharing=locked \
    --mount=type=secret,id=pip,dst=/etc/pip.conf \
    pip install -r "requirements/$(if [ "$DJANGO_ENV" = "production" ]; then echo "production.txt"; else echo "development.txt"; fi)"

COPY ./docker/django/docker-entrypoint.sh /docker-entrypoint.sh

RUN chmod +x "/docker-entrypoint.sh" \
  # Replacing line separator CRLF with LF for Windows users:
    && sed -i "s/\r$//g" "/docker-entrypoint.sh"

# The following stage is for pre-commit hook in Gitlab CI
FROM development_build AS entrypoint_build

USER web

ENTRYPOINT ["sh", "/docker-entrypoint.sh"]

# The following stage is only for Prod:
# https://wemake-django-template.readthedocs.io/en/latest/pages/template/production.html
FROM entrypoint_build as production_build

COPY --chown=web:web . .
