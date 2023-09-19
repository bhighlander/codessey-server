#!/bin/bash

python manage.py loaddata categories
python manage.py loaddata entries
python manage.py loaddata comments
python manage.py loaddata todos

# run seed_users, register new user, then run seed_data