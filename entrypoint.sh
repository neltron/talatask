#!/bin/sh -ex

python manage.py migrate --no-input
python manage.py collectstatic --no-input
gunicorn --worker-tmp-dir /dev/shm --workers=2 --threads=4 --worker-class=gthread --preload --bind 0.0.0.0:8000 talatask.wsgi:application

tail -f /dev/null
