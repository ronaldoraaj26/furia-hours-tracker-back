#!/bin/sh
set -e

echo "Waiting for MySQL..."
while ! nc -z "$MYSQL_HOST" "$MYSQL_PORT"; do
  sleep 1
done

echo "MySQL is up."

echo "Running migrations..."
until python manage.py migrate --fake-initial --noinput; do
  echo "Migration failed, retrying in 3 seconds..."
  sleep 3
done

exec python manage.py runserver 0.0.0.0:8000
