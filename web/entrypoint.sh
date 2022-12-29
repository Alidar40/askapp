#!/bin/sh

python manage.py migrate --no-input

# python manage.py collectstatic --no-input

# gunicorn languages.wsgi:application --bind 0.0.0.0:8000
gunicorn -c testconf.py askapp.wsgi
