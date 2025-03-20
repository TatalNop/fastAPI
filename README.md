# FastAPI
## Start
```
docker-compose up --build

```
## API Endpoints Example
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
