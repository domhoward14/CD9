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
curl -X PATCH -d '{"auth_code" : "4/nzOdrbQIUmJLVQG0V19z5GTu2CLDxPW-fPDarn8X1QY"}' -H "Content-Type: application/json" -H "Authorization: Token 9ff246b2123e942d782af89c106cb6d2f018a72d" http://127.0.0.1:8000/CD9/api/update_profile/164851885831702/ > output.html

GET TEEN AND PARENT ID
curl -H "Authorization: Token bf484b516de1a402e822faf777ede33436ce1c98" http://127.0.0.1:8000/CD9/api/get_ids/ > output.html

CURRENT USER INFO
{"token": "bf484b516de1a402e822faf777ede33436ce1c98", "success": true}
"""

"""
Misc
Server Client ID -> 53665769505-bp4qm9qb1e8b5d2csrqtanib9i9fei4m.apps.googleusercontent.com
Client Secret -> U_nBrZxrJO3gRDkW52caEXqo
"""