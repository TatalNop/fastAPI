
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
import jwt
from jwt import PyJWKClient
from config.config_file import OIDC_CONFIG

AUTH0_DOMAIN = OIDC_CONFIG['domain']
ALGORITHMS = OIDC_CONFIG['algorithms']
API_AUDIENCE = OIDC_CONFIG['audience']

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        JWKS_URL = f'https://{AUTH0_DOMAIN}/.well-known/jwks.json'
        jwks_client = PyJWKClient(JWKS_URL)
        signing_key = jwks_client.get_signing_key_from_jwt(token).key
        payload = jwt.decode(
                token,
                signing_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer=f"https://{AUTH0_DOMAIN}/"
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")