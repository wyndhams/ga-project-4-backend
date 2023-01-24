#!/bin/bash

echo "dropping database django-festi"
dropdb django-festi

echo "creating database django-festi"
createdb django-festi

python manage.py makemigrations

python manage.py migrate

echo "inserting users"
python manage.py loaddata jwt_auth/seeds.json

echo "inserting genres"
python manage.py loaddata genres/seeds.json

echo "inserting artists"
python manage.py loaddata artists/seeds.json

echo "inserting festivals"
python manage.py loaddata festivals/seeds.json

echo "inserting reviews"
python manage.py loaddata reviews/seeds.json