#bash testing scripts for django server and api endpoints
"""
CREATE USER
curl -X POST -d '{"token" : "CAACv91mPJ2IBAL7hQEQVShRFi9p0rVSZCcZBP38LdE4q9rUkZAhJoeZBL1SywgltwFE3a5nRHXuZA0ef2zH59sb1gIZAAjrHSUSMRyzVWicQf0svHJPOm2xDBFynObVlqwXfaiNE3rT1dj7hz6mokQlZBXBInwZAlVoPCU8e7zoomZBy9d0ugoAiyff7jgSfiQ54tnIVCvZBBZCCQZDZD"}' http://127.0.0.1:8000/CD9/api/new_user/ > output.html

CREATE TEXT
curl -X POST -d '{"number":5555555555,"date":"2016-01-15T04:34:10.105491Z", "content":"this is only a test"}' -H "Content-Type: application/json" -H "Authorization: Token 62b7075503b7800544405ead70822577f72feebc" http://127.0.0.1:8000/CD9/api/texts/ > output.html

CREATE APP
curl -X POST -d '{"installDate":"2016-01-15T04:34:10.105491Z", "appName" : "facebook"}' -H "Content-Type: application/json" -H "Authorization: Token 55ae31b5600f8a6a3a1369fd30e1ba1d3efb41c2" http://127.0.0.1:8000/CD9/api/apps/ > output.html


CREATE PHONE CALL
curl -X POST -d '{"number" : 444444444, "convoTime" : 33, "date" : "2016-01-15T04:34:10"}' -H "Content-Type: application/json" -H "Authorization: Token 55ae31b5600f8a6a3a1369fd30e1ba1d3efb41c2" http://127.0.0.1:8000/CD9/api/phone_calls/ > output.html

CREATE WEB HISTORY
curl -X POST -d '{"site":"facebook.com" , "date" : "2016-01-15T04:34:10.105491Z" , "rating" : 10}' -H "Content-Type: application/json" -H "Authorization: Token 55ae31b5600f8a6a3a1369fd30e1ba1d3efb41c2" http://127.0.0.1:8000/CD9/api/web_history/ > output.html

CREATE PARENT
curl -X POST -d '{"username" : "uncle" , "password" : "password", "email" : "uncle@email.com"}' -H "Content-Type: application/json" -H "Authorization: Token 55ae31b5600f8a6a3a1369fd30e1ba1d3efb41c2" http://127.0.0.1:8000/CD9/api/add_parent/ > output.html

CURRENT USER INFO
{"token": "55ae31b5600f8a6a3a1369fd30e1ba1d3efb41c2", "success": true}
"""

