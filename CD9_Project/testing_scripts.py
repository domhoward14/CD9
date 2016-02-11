#bash testing scripts for django server and api endpoints
"""
CREATE USER
curl -X POST -d '{"token" : "CAACEdEose0cBACQRrbwRqhOcb1v0Tyw8gnvNKUISCFwCT4ZCEanlXZBxksD5xSNaRkBmBZCqKUC6XHgjZBtMZCciPH4iIT1RbYuN8emwq1fg0m4zMShopxsMZB46PlSuJ5ZAhQXxafpN2SZCenlSoEOKAkU7U306bpTylRpVZCXRj2rHeoN8pAHukUlriq7gxW6eGkUswEnVrKAZDZD"}' http://127.0.0.1:8000/CD9/api/new_user/ > output.html

CREATE TEXT
curl -X POST -d '{"number":5555555555,"date":"2016-01-15T04:34:10.105491Z", "content":"this is only a test"}' -H "Content-Type: application/json" -H "Authorization: Token 62b7075503b7800544405ead70822577f72feebc" http://127.0.0.1:8000/CD9/api/texts/ > output.html

CREATE APP
curl -X POST -d '{"installDate":"2016-01-15T04:34:10.105491Z", "appName" : "facebook"}' -H "Content-Type: application/json" -H "Authorization: Token 55ae31b5600f8a6a3a1369fd30e1ba1d3efb41c2" http://127.0.0.1:8000/CD9/api/apps/ > output.html


CREATE PHONE CALL
curl -X POST -d '{"number" : 444444444, "convoTime" : 33, "date" : "2016-01-15T04:34:10"}' -H "Content-Type: application/json" -H "Authorization: Token 55ae31b5600f8a6a3a1369fd30e1ba1d3efb41c2" http://127.0.0.1:8000/CD9/api/phone_calls/ > output.html

CREATE WEB HISTORY
curl -X POST -d '{"site":"facebook.com" , "date" : "2016-01-15T04:34:10.105491Z" , "rating" : 10}' -H "Content-Type: application/json" -H "Authorization: Token 55ae31b5600f8a6a3a1369fd30e1ba1d3efb41c2" http://127.0.0.1:8000/CD9/api/web_history/ > output.html

CREATE PARENT
curl -X POST -d '{"username" : "uncle" , "password" : "password", "email" : "uncle@email.com"}' -H "Content-Type: application/json" -H "Authorization: Token f7864c737d6442b314797c1aab8f4288654fb71b" http://127.0.0.1:8000/CD9/api/add_parent/ > output.html

UPDATE USER INFO
curl -X PATCH -d '{"google_token" : "PLACETOKENHERE"}' -H "Content-Type: application/json" -H "Authorization: Token f7864c737d6442b314797c1aab8f4288654fb71b" http://127.0.0.1:8000/CD9/api/update_profile/USER_ID_HERE/ > output.html

GET TEEN AND PARENT ID
curl -H "Authorization: Token f7864c737d6442b314797c1aab8f4288654fb71b" http://127.0.0.1:8000/CD9/api/get_ids/ > output.html


CURRENT USER INFO
{"token": "f7864c737d6442b314797c1aab8f4288654fb71b", "success": false}

need to store google tokens

"""

