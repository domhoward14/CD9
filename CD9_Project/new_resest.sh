#!/bin/bash

rm -f db.sqlite3
python manage.py migrate
chmod 666 /home/domhoward14/CD9/CD9/CD9_Project/db.sqlite3
