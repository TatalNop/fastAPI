# FastAPI
![Image](https://github.com/user-attachments/assets/1c7d4799-dbb9-420a-aa99-e9daedf273ea)

## Start
```
docker-compose up --build
```
## Swagger UI
```
http://localhost:8000/docs (Backend for Frontend)
http://localhost:8001/docs (Login Service)
http://localhost:8002/docs (Users Servive)
http://localhost:8003/docs (Posts Service)
```
## API Endpoints
```
#BFF
Method POST : http://localhost:8000/bff/login/access_token ( Login "client_id.txt" Get Access Token )
Method GET : http://localhost:8000/bff/get/all_users ( List All User )
Method GET : http://localhost:8000/bff/bff/users/pagination ( List User Pagination )
Method GET : http://localhost:8000/bff/posts/all ( List All Post )
Method PUT : http://localhost:8000/bff/users ( Update Existing User By User Id )
Method DELETE : http://localhost:8000/bff/users ( Delete User By User Id)

Method GET : http://localhost:8000/bff/get/all_posts ( List All Post )
Method GET : http://localhost:8000/bff/posts/search ( List All Post By User Id )
Method POST : http://localhost:8000/bff/add/posts ( Add New Post By User Id )
Method PUT : http://localhost:8000/bff/posts ( Update Existing Post By Post Id )
Method DELETE : http://localhost:8000/bff/posts ( Delete Post By Post Id)
```
## Example Call API
```
curl -X POST "http://localhost:8000/bff/login/token" \
     -H "Content-Type: application/json" \
     -d '{
          "client_id": "your_client_id",
          "client_secret": "your_client_secret"
         }'

curl -X GET "http://localhost:8000/bff/users/all" -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```
