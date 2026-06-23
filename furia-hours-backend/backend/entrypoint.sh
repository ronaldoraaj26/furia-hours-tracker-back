#!/bin/sh
set -e

echo "Waiting for MySQL..."
while ! nc -z "$MYSQL_HOST" "$MYSQL_PORT"; do
  sleep 1
 done

echo "MySQL is up."
python manage.py migrate --noinput
python manage.py runserver 0.0.0.0:8000
