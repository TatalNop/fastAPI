from fastapi import FastAPI,HTTPException
from config.schemas import Token, TokenRequest
from config.config_file import OIDC_CONFIG
from database.database import database_create
import requests

app = FastAPI()
database_create()

@app.post("/login", response_model=Token)
async def get_token(request :TokenRequest):
    token_url = OIDC_CONFIG["token_url"]
    data = {
        "grant_type": OIDC_CONFIG["grant_type"],
        "client_id": request.client_id,
        "client_secret": request.client_secret,
        "audience": OIDC_CONFIG["audience"]
    }
    try:
        response = requests.post(token_url, data=data)
        response.raise_for_status() 
        token = response.json()
        if "error" in token:
            raise HTTPException(status_code=401, detail=f"Authentication failed: {token.get('error_description')}")
        return token
    except requests.exceptions.HTTPError as http_err:
        raise HTTPException(status_code=400, detail=f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as err:
        raise HTTPException(status_code=500, detail=f"Request error occurred: {err}")
