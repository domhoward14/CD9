#!/bin/bash

rm -f db.sqlite3
python manage.py migrate
curl -i \
-H "Accept: application/json" \
-H "Content-Type:application/json" \
-X POST --data '{"token" :"'"$1"'"}'  http://127.0.0.1:8000/CD9/api/new_user/   > teenOutput.html
token=`cat teenOutput.html | egrep "\{.*\}" | awk '{print $2}' | cut -d\" -f 2`
echo "the token is  $token"
curl -X POST -d '{"username" : "uncle" , "password" : "password", "email" : "uncle@email.com"}' -H "Content-Type: application/json" -H "Authorization: Token $token" http://127.0.0.1:8000/CD9/api/add_parent/ > output.html


