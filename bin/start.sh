#!/usr/bin/env sh

#if [[ ! -d 'tmp' ]]; then
#  mkdir -p tmp
#fi

#if [[ "$APP_ENV" != 'dev' && ! -d  "shopping_app/tmp/db.shopping_app.sqlite3" ]]; then
#  touch shopping_app/tmp/db.shopping_app.sqlite3
#fi

cd shopping_app

# Run migrations and start server
python manage.py migrate && python manage.py runserver "0.0.0.0:8000"
