#bash testing scripts for django server and api endpoints
"""
CREATE USER
curl -X POST -d '{"token" : "CAACv91mPJ2IBAMZBLCar8UeTXIZATLiYw8ZBEAllgzhZBJ4tG7OS3Ia3ZAcUf7OIjPYnL0kne23NGLDNGwWLzuAXNZAi9fVhaaB7oEANwziw8Vup13ihiaUqSKNbhgTuhC7mwskFN5tgmlL9vlk4oN9ZBDLZAWcclsBwwCm2rkZBwEgZBmx09VEQIaK3lJPUZCbrnxatzLY6Do0LgZDZD"}' http://127.0.0.1:8000/CD9/api/new_user/ > output.html

CREATE TEXT
curl -X POST -d '[{"number":4521435,"date":"2016-01-15T04:34:10.105491Z", "content":"this is only a test"}]' -H "Content-Type: application/json" -H "Authorization: Token d034bc651d3fd47c3518a4f54eab1d92a46cd383" http://127.0.0.1:8000/CD9/api/texts/ > output.html

CREATE APP
curl -X POST -d '[{"packageName" : "com.snapchat.android", "installDate":"2016-01-15T04:34:10.105491Z"}]' -H "Content-Type: application/json" -H "Authorization: Token d034bc651d3fd47c3518a4f54eab1d92a46cd383" http://127.0.0.1:8000/CD9/api/apps/ > output.html

CREATE PHONE CALL
curl -X POST -d '[{"number" : 4521435, "convoTime" : 33, "date" : "2016-01-15T04:34:10"}]' -H "Content-Type: application/json" -H "Authorization: Token 089bd7c41441b5b5f1b5441b274839619fc39d7d" http://127.0.0.1:8000/CD9/api/phone_calls/ > output.html

CREATE WEB HISTORY
curl -X POST -d '[{"site":"fox.com" , "installDate" : "2016-01-15T04:34:10.105491Z"}] ' -H "Content-Type: application/json" -H "Authorization: Token 089bd7c41441b5b5f1b5441b274839619fc39d7d" http://127.0.0.1:8000/CD9/api/web_history/ > output.html

CREATE PARENT
curl -X POST -d '{"username" : "uncle" , "password" : "password", "email" : "uncle@email.com"}' -H "Content-Type: application/json" -H "Authorization: Token 15a371f9b4d54eed58cdc49c304f01ed17ddb630" http://127.0.0.1:8000/CD9/api/add_parent/ > output.html

UPDATE USER INFO
curl -X PATCH -d '{"gcm_reg_id" : "cFB5VC4vZVo:APA91bHpB3HxyCLrMXBtE3W-rqVJLFKenDB_X_1nOBp0mZ-70PvXVpJZbymsD_e96K7Bqnhh-9lVeSI6WZfATy_yfWbU82cR5sxSyCzPxnt43WfWrt2nrmuusLXA67IAa4txWqT1zHpZ"}' -H "Content-Type: application/json" -H "Authorization: Token 1aa619689b45d540778d335414c803abd1b49571" http://127.0.0.1:8000/CD9/api/update_profile/USER_ID_HERE/ > output.html

GET TEEN AND PARENT ID
curl -H "Authorization: Token 1aa619689b45d540778d335414c803abd1b49571" http://127.0.0.1:8000/CD9/api/get_ids/ > output.html

CURRENT USER INFO
{"token": "3d866ff27657f91b0cde032e091114f8e36ca73b", "success": true}
"""

"""
TODO
use the site api and app site api
social media data collection
google api’s and push notifications
    figure out what information is needed during registration time
    long lived tokens
"""