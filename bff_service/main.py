from fastapi import FastAPI, Depends, HTTPException,Query
import httpx
from config.verify import verify_token
from config.schemas import PostsIn, TokenRequest,Users
from config.config_file import OIDC_CONFIG

# Auth0 Configurations
#AUTH0_DOMAIN = "dev-mkmcn247grdl7y20.us.auth0.com"
#API_AUDIENCE = "https://backend_login_api.com"
#ALGORITHMS = ["RS256"]
AUTH0_DOMAIN = OIDC_CONFIG['domain']
ALGORITHMS = OIDC_CONFIG['algorithms']
API_AUDIENCE = OIDC_CONFIG['audience']
JWKS_URL = f"https://{AUTH0_DOMAIN}/.well-known/jwks.json"

app = FastAPI()
    
@app.post("/bff/login/token")
async def login_get_token(resuest : TokenRequest):
    url = f"http://127.0.0.1:8001/login"
    async with httpx.AsyncClient() as client:
        response = await client.post(url,
                                     json={
                                         "client_id": resuest.client_id, 
                                         "client_secret": resuest.client_secret})
    return response.json()

@app.get("/bff/users/all")
async def list_users_all(token: dict = Depends(verify_token)):
    url = f"http://127.0.0.1:8002/users/all"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
    return response.json()

@app.get("/bff/users/pagination",response_model=list[Users])
async def list_user_pagination(page: int = Query(1, ge=1), per_page: int = Query(3, ge=1), token: dict = Depends(verify_token)):
    start = (page - 1) * per_page
    end = start + per_page
    url = f"http://127.0.0.1:8002/users/all"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
    user_data = response.json()
    paginated_data = user_data[start:end]
    return paginated_data

@app.get("/bff/posts/all")
async def get_post_all(token: dict = Depends(verify_token)):
    url = f"http://127.0.0.1:8003/posts/all"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
    return response.json()

@app.get("/bff/posts/search")
async def get_post_by_user(username : str, token: dict = Depends(verify_token)):
    url = f'http://127.0.0.1:8003/posts/user?username={username}'
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
    return response.json()

@app.post("/bff/posts/add")
async def add_post_by_user(post_data : PostsIn, token: dict = Depends(verify_token)):
    url = f'http://127.0.0.1:8003/posts/add'
    async with httpx.AsyncClient() as client:
        response = await client.post(url,
                                    json={"username" : post_data.username, 
                                          "body" : post_data.body,
                                          "title" : post_data.title})
    return response.json()