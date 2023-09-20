#!/bin/bash

rm db.sqlite3
rm -rf ./codesseyapi/migrations
python manage.py makemigrations codesseyapi
python manage.py migrate
python manage.py loaddata users
python manage.py loaddata tokens
python manage.py loaddata programmers

# run seed_users, register new user, then run seed_data