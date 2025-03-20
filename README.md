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
Method POST : http://localhost:8000/bff/login/token ( Login Get Token Using )
Method GET : http://localhost:8000/bff/users/all ( List All User Authentication Token )
Method GET : http://localhost:8000/bff/users/pagination ( List User Pagination )
Method GET : http://localhost:8000/bff/posts/all ( List All Post )
Method GET : http://localhost:8000/bff/posts/search ( List All Post By Username )
Method POST : http://localhost:8000/bff/posts/add ( Add New Post For Existing Username )
Method PUT : http://localhost:8000/bff/users/user_id ( Update Existing Username By User Id )
Method DELETE : http://localhost:8000/bff/users/user_id ( Delete Existing Username By User Id)
Method PUT :  http://localhost:8000/bff/posts/post_id ( Update Existing Post By Post Id )
Method DELETE :  http://localhost:8000/bff/posts/post_id ( Delete Existing Post By Post Id )
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
