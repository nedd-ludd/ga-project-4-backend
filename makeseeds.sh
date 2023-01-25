#!/bin/bash

# drop and make db manually in pg admin

python manage.py makemigrations

python manage.py migrate

# echo "inserting users"
# python manage.py loaddata jwt_auth/seeds.json

echo "inserting categories"
python manage.py loaddata categories/seeds.json

