#!/bin/sh

cd ../drums_practice_logs/drums_practice_logs
python manage.py makemigrations
python manage.py migrate
uwsgi --http :8000 --workers 4 --master --enable-threads --module drums_practice_logs.wsgi
