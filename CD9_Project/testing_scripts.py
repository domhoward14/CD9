#bash testing scripts for django server and api endpoints
"""
CREATE USER
curl -X POST -d '{"token" : "CAACv91mPJ2IBAGJzxoShq6fAFDgi6YlEM52iDZASDHUTVf7XbXsd7tPWeximiIQNTv6iMeV1MxAe0oCrH6T4dZBtvAgZBwBdXg9VWgccVYGZAFP3EXsGFPs19QZAhViplXCjFpbVemJToIhnUEUZC8xZADZA28IABM8djvCZCHUmV5SYWNkZA2pqjNs2FVkVcoQxRs1Po4dmfEdwZDZD"}' http://127.0.0.1:8000/CD9/api/new_user/ > output.html

CREATE TEXT
curl -X POST -d '{"number":5555555555,"date":"2016-01-15T04:34:10.105491Z", "content":"this is only a test"}' -H "Content-Type: application/json" -H "Authorization: Token 5c4024a4883736bea6f2ff28c9bce458e1d27a05" http://127.0.0.1:8000/CD9/api/texts/ > output.html

CREATE APP
curl -X POST -d '{"installDate":"2016-01-15T04:34:10.105491Z", "appName" : "facebook"}' -H "Content-Type: application/json" -H "Authorization: Token 55ae31b5600f8a6a3a1369fd30e1ba1d3efb41c2" http://127.0.0.1:8000/CD9/api/apps/ > output.html


CREATE PHONE CALL
curl -X POST -d '{"number" : 444444444, "convoTime" : 33, "date" : "2016-01-15T04:34:10"}' -H "Content-Type: application/json" -H "Authorization: Token 55ae31b5600f8a6a3a1369fd30e1ba1d3efb41c2" http://127.0.0.1:8000/CD9/api/phone_calls/ > output.html

CREATE WEB HISTORY
curl -X POST -d '{"site":"facebook.com" , "date" : "2016-01-15T04:34:10.105491Z" , "rating" : 10}' -H "Content-Type: application/json" -H "Authorization: Token 55ae31b5600f8a6a3a1369fd30e1ba1d3efb41c2" http://127.0.0.1:8000/CD9/api/web_history/ > output.html

CREATE PARENT
curl -X POST -d '{"username" : "uncle" , "password" : "password", "email" : "uncle@email.com"}' -H "Content-Type: application/json" -H "Authorization: Token 5c4024a4883736bea6f2ff28c9bce458e1d27a05" http://127.0.0.1:8000/CD9/api/add_parent/ > output.html

UPDATE USER INFO
curl -X PATCH -d '{"google_token" : "PLACETOKENHERE"}' -H "Content-Type: application/json" -H "Authorization: Token f7864c737d6442b314797c1aab8f4288654fb71b" http://127.0.0.1:8000/CD9/api/update_profile/USER_ID_HERE/ > output.html

GET TEEN AND PARENT ID
curl -H "Authorization: Token ec746241ea3c2118f8c325dd66912d8638ff66ff" http://127.0.0.1:8000/CD9/api/get_ids/ > output.html

CURRENT USER INFO
{"token": "5c4024a4883736bea6f2ff28c9bce458e1d27a05", "success": true}


"""

"""
TODO
use the site api and app site api
social media data collection
google api’s and push notifications
    figure out what information is needed during registration time
    long lived tokens
"""