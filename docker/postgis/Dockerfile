FROM postgres:17-bookworm

RUN apt-get update -y \
    && apt-get install -y --no-install-recommends \
    postgis \
    postgresql-17-postgis-3 \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && apt-get clean -y && rm -rf /var/lib/apt/lists/*

COPY ./db.sql /docker-entrypoint-initdb.d/
