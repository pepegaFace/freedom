#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

#python freedom/manage.py flush --no-input
python manage.py makemigrations academ
python manage.py migrate academ
python manage.py makemigrations freedom
python manage.py migrate freedom
python manage.py makemigrations kolotok
python manage.py migrate kolotok
python manage.py makemigrations
python manage.py migrate
python manage.py user_generator
python manage.py content_generator

exec "$@"
