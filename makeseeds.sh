#!/bin/bash

echo "creating festivals/seeds.json"
python manage.py dumpdata festivals --output festivals/seeds.json --indent=2;

echo "creating artists/seeds.json"
python manage.py dumpdata artists --output artists/seeds.json --indent=2;

echo "creating genres/seeds.json"
python manage.py dumpdata genres --output genres/seeds.json --indent=2;

echo "creating reviews/seeds.json"
python manage.py dumpdata reviews --output reviews/seeds.json --indent=2;

echo "creating jwt_auth/seeds.json"
python manage.py dumpdata jwt_auth --output jwt_auth/seeds.json --indent=2;