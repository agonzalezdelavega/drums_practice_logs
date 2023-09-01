#!/bin/sh

python manage.py collectstatic --no-input
python manage.py makemigrations
python manage.py migrate
uwsgi --socket :8000 --workers 2 --master --enable-threads --module drums_practice_logs.wsgi