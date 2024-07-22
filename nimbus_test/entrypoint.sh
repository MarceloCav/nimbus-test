#!/bin/sh

python wait_for_db.py

python manage.py makemigrations

python manage.py migrate

python manage.py runserver_tcp &

python manage.py runserver 0.0.0.0:8000

