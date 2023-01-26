#!/bin/bash

# drop and make db manually in pg admin

python manage.py makemigrations

python manage.py migrate


echo "inserting categories"
python manage.py loaddata categories/seeds.json

echo "inserting users"
python manage.py loaddata jwt_auth/seeds.json

echo "inserting items"
python manage.py loaddata items/seeds.json

