#!/bin/sh

python manage.py migrate --no-input

# python manage.py filldb --all 10

# python manage.py collectstatic --no-input

gunicorn -c testconf.py askapp.wsgi
