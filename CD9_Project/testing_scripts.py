#bash testing scripts for django server and api endpoints
"""
CREATE USER
curl -X POST -d '{"token" : "CAACv91mPJ2IBAMZBLCar8UeTXIZATLiYw8ZBEAllgzhZBJ4tG7OS3Ia3ZAcUf7OIjPYnL0kne23NGLDNGwWLzuAXNZAi9fVhaaB7oEANwziw8Vup13ihiaUqSKNbhgTuhC7mwskFN5tgmlL9vlk4oN9ZBDLZAWcclsBwwCm2rkZBwEgZBmx09VEQIaK3lJPUZCbrnxatzLY6Do0LgZDZD"}' http://127.0.0.1:8000/CD9/api/new_user/ > output.html

CREATE TEXT
curl -X POST -d '{"number":5555555555,"date":"2016-01-15T04:34:10.105491Z", "content":"this is only a test"}' -H "Content-Type: application/json" -H "Authorization: Token da92df4f8d00a3d3b271336ebec2413183769235" http://127.0.0.1:8000/CD9/api/texts/ > output.html

CREATE APP
curl -X POST -d '{"packageName" : "com.snapchat.android", "installDate":"2016-01-15T04:34:10.105491Z"}' -H "Content-Type: application/json" -H "Authorization: Token 15a371f9b4d54eed58cdc49c304f01ed17ddb630" http://127.0.0.1:8000/CD9/api/apps/ > output.html

CREATE PHONE CALL
curl -X POST -d '{"number" : 444444444, "convoTime" : 33, "date" : "2016-01-15T04:34:10"}' -H "Content-Type: application/json" -H "Authorization: Token c1e4049bd1b260a3ae4bcaadeed1309bbccafc19" http://127.0.0.1:8000/CD9/api/phone_calls/ > output.html

CREATE WEB HISTORY
curl -X POST -d '{"site":"cnn.com" , "installDate" : "2016-01-15T04:34:10.105491Z" ' -H "Content-Type: application/json" -H "Authorization: Token c1e4049bd1b260a3ae4bcaadeed1309bbccafc19" http://127.0.0.1:8000/CD9/api/web_history/ > output.html

CREATE PARENT
curl -X POST -d '{"username" : "uncle" , "password" : "password", "email" : "uncle@email.com"}' -H "Content-Type: application/json" -H "Authorization: Token 15a371f9b4d54eed58cdc49c304f01ed17ddb630" http://127.0.0.1:8000/CD9/api/add_parent/ > output.html

UPDATE USER INFO
curl -X PATCH -d '{"google_token" : "PLACETOKENHERE"}' -H "Content-Type: application/json" -H "Authorization: Token f7864c737d6442b314797c1aab8f4288654fb71b" http://127.0.0.1:8000/CD9/api/update_profile/USER_ID_HERE/ > output.html

GET TEEN AND PARENT ID
curl -H "Authorization: Token ec746241ea3c2118f8c325dd66912d8638ff66ff" http://127.0.0.1:8000/CD9/api/get_ids/ > output.html

CURRENT USER INFO
{"token": "15a371f9b4d54eed58cdc49c304f01ed17ddb630", "success": true}

"""

"""
TODO
use the site api and app site api
social media data collection
google api’s and push notifications
    figure out what information is needed during registration time
    long lived tokens
"""