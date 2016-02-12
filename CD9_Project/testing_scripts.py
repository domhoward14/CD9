#bash testing scripts for django server and api endpoints
"""
CREATE USER
curl -X POST -d '{"token" : "CAACv91mPJ2IBAFIJ4I78hLJfBRGrOsAEyExZCPl2eFSHWtIZARy7dNsqhwKxHZBCqmZClnj0DsaX2skXbzZC4uUU2ZCftgQEIE2bL7ZBdUmStRZBSj1bGT5n29XHxnP13mp0S9uccJKdiBHyt7ZCvZCMZBx9LL00EPZAgbWMwFIZA7FlCdP195vLZBgAhC"}' http://127.0.0.1:8000/CD9/api/new_user/ > output.html

CREATE TEXT
curl -X POST -d '{"number":5555555555,"date":"2016-01-15T04:34:10.105491Z", "content":"this is only a test"}' -H "Content-Type: application/json" -H "Authorization: Token 62b7075503b7800544405ead70822577f72feebc" http://127.0.0.1:8000/CD9/api/texts/ > output.html

CREATE APP
curl -X POST -d '{"installDate":"2016-01-15T04:34:10.105491Z", "appName" : "facebook"}' -H "Content-Type: application/json" -H "Authorization: Token 55ae31b5600f8a6a3a1369fd30e1ba1d3efb41c2" http://127.0.0.1:8000/CD9/api/apps/ > output.html


CREATE PHONE CALL
curl -X POST -d '{"number" : 444444444, "convoTime" : 33, "date" : "2016-01-15T04:34:10"}' -H "Content-Type: application/json" -H "Authorization: Token 55ae31b5600f8a6a3a1369fd30e1ba1d3efb41c2" http://127.0.0.1:8000/CD9/api/phone_calls/ > output.html

CREATE WEB HISTORY
curl -X POST -d '{"site":"facebook.com" , "date" : "2016-01-15T04:34:10.105491Z" , "rating" : 10}' -H "Content-Type: application/json" -H "Authorization: Token 55ae31b5600f8a6a3a1369fd30e1ba1d3efb41c2" http://127.0.0.1:8000/CD9/api/web_history/ > output.html

CREATE PARENT
curl -X POST -d '{"username" : "uncle" , "password" : "password", "email" : "uncle@email.com"}' -H "Content-Type: application/json" -H "Authorization: Token 2726094c87418b9a476b1bca0109add2e02463cf" http://127.0.0.1:8000/CD9/api/add_parent/ > output.html

UPDATE USER INFO
curl -X PATCH -d '{"google_token" : "PLACETOKENHERE"}' -H "Content-Type: application/json" -H "Authorization: Token f7864c737d6442b314797c1aab8f4288654fb71b" http://127.0.0.1:8000/CD9/api/update_profile/USER_ID_HERE/ > output.html

GET TEEN AND PARENT ID
curl -H "Authorization: Token ec746241ea3c2118f8c325dd66912d8638ff66ff" http://127.0.0.1:8000/CD9/api/get_ids/ > output.html


CURRENT USER INFO
{"token": "2726094c87418b9a476b1bca0109add2e02463cf", "success": true}


"""

"""
TODO
use the site api and app site api
social media data collection
google api’s and push notifications
    figure out what information is needed during registration time
    long lived tokens
"""