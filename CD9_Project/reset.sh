#!/bin/bash

rm -f db.sqlite3
python manage.py migrate
curl -X POST -d "{"token" : $1}" http://127.0.0.1:8000/CD9/api/new_user/ > output.html

