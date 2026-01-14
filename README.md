# vi-learn-docker

[VI] Learn Docker

# Development

## Local development

* Create virtual environment
```bash
python -m venv env
```
or
```bash
virtualenv env
```

* Install packages
```bash
env\bin\pip install -r requirements\development.txt
```

* Set necessary environment variables in `.env` file (like connection to database and e.t.c)

* (Optional) Change `config\settings\local.py` (with your own settings).

* Run commands:
```bash
env\bin\python manage.py migrate
env\bin\python manage.py runserver
```

## Development with docker
* Set environment variables in `docker/postgres/.env`
* Set necessary environment variables in `.env` file (like connection to database and e.t.c)
* Run commands:
```bash
docker-compose build
docker-compose run --rm web python manage.py migrate
# Create superueser if it necessary
docker-compose run --rm web python manage.py createsuperuser
docker-compose up
```

# Migrate data
If you have a new database, you might load initial data.

On source server run command
```bash
python manage.py dumpdata --all --format json --indent 4 --natural-primary --natural-foreign --output data.json --exclude session
```
On dest server run command
```bash
python manage.py loaddata data.json
```
More information see: [Initial data](https://docs.djangoproject.com/en/3.2/howto/initial-data/)


# Localization
Run command
```bash
env\bin\python manage.py makemessages -l ru -i env -i *.pyc
```
Then translate the file `.\locale\ru\LC_MESSAGES\django.po` 
On development or production server run command
```bash
env\bin\python manage.py compilemessages -l ru
```

# Contributing

Before send your changes in original repository you SHOULD run `docker/ci.sh` command for check

# How to...

## How to increase version
You should run next command for increase version
```bash
bumpversion --verbose major|minor|patch
```
