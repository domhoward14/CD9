curl -i \
-H "Accept: application/json" \
-H "Content-Type:application/json" \
-X POST --data '{"token" :"'"$1"'"}'  http://127.0.0.1:8000/CD9/api/new_user/   > output.html
