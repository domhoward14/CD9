#bash testing scripts for django server and api endpoints
"""
CREATE USER
curl -X POST -d '{"token" : "CAACv91mPJ2IBAPQPCZCOUUG41fYU8HdFHfesQ1xhYf0y1j1fchpueiNSHcBBJ9tjpW1DzuNEJpTtP3D4azpZA7W7UqRVmWDGZB00Xd8E4RxHlDBRZB6yyZC08CE0cRA3w2q00EQGhlAU4GBxndccJheR9qkShZADaW85NZCjc3KxetZBNFWXqmDg9kvBRaIS3sLy1Tzdx6ZBvfwZDZD"}' http://127.0.0.1:8000/CD9/api/new_user/ > output.html
CREATE TEXT
curl -X POST -d '[{"number":4521435,"date":"2016-01-15T04:34:10.105491Z", "content":"this is only a test"}]' -H "Content-Type: application/json" -H "Authorization: Token d034bc651d3fd47c3518a4f54eab1d92a46cd383" http://127.0.0.1:8000/CD9/api/texts/ > output.html
CREATE APP
curl -X POST -d '[{"packageName" : "com.snapchat.android", "installDate":"2016-01-15T04:34:10.105491Z"}]' -H "Content-Type: application/json" -H "Authorization: Token d034bc651d3fd47c3518a4f54eab1d92a46cd383" http://127.0.0.1:8000/CD9/api/apps/ > output.html
CREATE PHONE CALL
curl -X POST -d '[{"number" : 4521435, "convoTime" : 33, "date" : "2016-01-15T04:34:10"}]' -H "Content-Type: application/json" -H "Authorization: Token 089bd7c41441b5b5f1b5441b274839619fc39d7d" http://127.0.0.1:8000/CD9/api/phone_calls/ > output.html
CREATE WEB HISTORY
curl -X POST -d '[{"site":"fox.com" , "installDate" : "2016-01-15T04:34:10.105491Z"}] ' -H "Content-Type: application/json" -H "Authorization: Token 089bd7c41441b5b5f1b5441b274839619fc39d7d" http://127.0.0.1:8000/CD9/api/web_history/ > output.html
CREATE PARENT
curl -X POST -d '{"username" : "uncle" , "password" : "password", "email" : "uncle@email.com"}' -H "Content-Type: application/json" -H "Authorization: Token "adf5bf2182555b5149fdd789263d90ac4e47f986" http://127.0.0.1:8000/CD9/api/add_parent/ > output.html
UPDATE USER INFO
curl -X PATCH -d '{"auth_code" : "4/nzOdrbQIUmJLVQG0V19z5GTu2CLDxPW-fPDarn8X1QY"}' -H "Content-Type: application/json" -H "Authorization: Token "9859803db5abd0d54576121da57dcbf300e6c85a"" http://127.0.0.1:8000/CD9/api/update_profile/164851885831702/ > output.html
GET TEEN AND PARENT ID
curl -H "Authorization: Token fde3bcd533ce553d835bdce5718da597d95cf7d8" http://127.0.0.1:8000/CD9/api/get_ids/ > output.html
PING THE SERVER
curl -X POST -d '{}' "Content-Type: application/json" -H "Authorization: Token 8335a0d27beea4eb32325d58f283010e0e936734" http://127.0.0.1:8000/CD9/api/ping/ 
ADD ANOTHER TEEN
curl -X PUT -d '{"username" : "uncle" , "password" : "password", "email" : "uncle@email.com"}' -H "Content-Type: application/json" -H "Authorization: Token a7c94ea22b45b7c6c5585319872bb3d21a941e54" http://127.0.0.1:8000/CD9/api/add_another_teen/416014220204790/ > output.html


{"token": "0c0d85984ac58c5a0b50be1709f9d210893a0573", "password": "6slkXOKpllCVPUmyDg2yMYzhlDpRbshYNZ5UXFDf7ZgeXsDKWa", "success": true}
{"token": "01dd92c47827397c13f99d790d0571873b0a054e", "password": "I9QBg3AYJ5hbFNgBUDmWojk4Ue2uSbilexCObrXErrqHVWGXzc", "success": true}{"token": "243de7a1a003c03a05bed2f80abbd96e279ab7b4", "password": "0RNdGkkaj363goy44BFb7wx2t6EyonmlbvQEFnQDli17XqYd7t", "success": false}{"token": "8388522ea9acbcda87d3c0d18f8c6f0fe7aa94ab", "password": "vzpadpGmSbvT2rgBuPWkxPpED1v3Pcp4AkPv4XZx4NBKzTv79A", "success": true}{"token": "b45c1dd02be15481ed562adb62b6747badd2f03f", "password": "zVQhfJABLz2EBrQVoaUSHTH5iibPqdvXxpSQ3etQv1LkTzIGiR", "success": true}