#! /bin/bash

chmod +x ./entrypoint.sh

python manage.py makemigrations --no-input

python manage.py migrate --no-input

python manage.py collectstatic --no-input

python manage.py create_su

exec gunicorn core.wsgi:application -b 0.0.0.0:8000 --reload