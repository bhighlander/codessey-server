#!/bin/bash

rm db.sqlite3
rm -rf ./codesseyapi/migrations
python manage.py makemigrations codesseyapi
python manage.py migrate
python manage.py loaddata users
python manage.py loaddata tokens
python manage.py loaddata programmers
python manage.py loaddata categories
python manage.py loaddata entries
python manage.py loaddata comments
python manage.py loaddata todos