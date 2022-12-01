#!/usr/bin/env sh

APP_ENV="${APP_ENV:-dev}"

if [[ -x "$(command -v docker)" &&"$APP_ENV" = 'dev' ]]; then
  echo 'Starting mailhog server in docker'
  docker run -it -d -p 1025:1025 -p 8025:8025 mailhog/mailhog
  echo << EMAIL
    EMAIL HOST: 127.0.0.1
    EMAIL PORT: 1025
EMAIL
fi

cd shopping_app

# Run migrations and start server
python manage.py migrate && python manage.py runserver "0.0.0.0:8000"
