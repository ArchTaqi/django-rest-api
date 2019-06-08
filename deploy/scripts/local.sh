#!/usr/bin/env bash
# sudo fuser -k 8000/tcp
killall python; python manage.py runserver [::]:8000

python manage.py dumpdata api.city --format=json > api/fixtures/city/initial_data.json
python manage.py dumpdata api.category --format=json > api/fixtures/category/initial_data.json
python manage.py dumpdata api.organization --format=json > api/fixtures/organization/initial_data.json

python manage.py loaddata api/fixtures/city/initial_data.json
python manage.py loaddata api/fixtures/category/initial_data.json
python manage.py loaddata api/fixtures/organization/initial_data.json

heroku run python manage.py migrate
heroku run python manage.py createsuperuser    # Nopass12345!
heroku run  python manage.py makemigrations petstore
python manage.py runserver
python manage.py test