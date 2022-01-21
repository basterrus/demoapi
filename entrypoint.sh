#! /bin/bash

chmod +x ./entrypoint.sh

python manage.py makemigrations --no-input

python manage.py migrate --no-input

#python manage.py runserver 127.0.0.1:8000

ls -al ./

exec ./core.wsgi:application -b 127.0.0.1:8000 --reload