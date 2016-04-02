#!/bin/bash

rm -f db.sqlite3
python manage.py migrate
chmod 666 /home/domhoward14/CD9/CD9/CD9_Project/db.sqlite3
curl -i \
-H "Accept: application/json" \
-H "Content-Type:application/json" \
-X POST --data '{"token" :"'"$1"'"}'  http://127.0.0.1:8000/CD9/api/new_user/   > teenOutput.html
token=`cat teenOutput.html | egrep "\{.*\}" | awk '{print $2}' | cut -d\" -f 2`
echo "the token is  $token"
curl -X POST -d '{"username" : "uncle" , "password" : "password", "email" : "uncle@email.com"}' -H "Content-Type: application/json" -H "Authorization: Token $token" http://127.0.0.1:8000/CD9/api/add_parent/ > output.html


