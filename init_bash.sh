#!/usr/bin/env bash

readonly virtual='/home/vubon/personal/django_boilerplate/venv/bin/activate'
# readonly virtual='/home/circle/.pyenv/versions/connect_demo_env/bin/activate'
source ${virtual}
python manage.py runscript clean_database_tables
python manage.py makemigrations
python manage.py migrate
python manage.py runscript enter_default_data
# python manage.py runserver
