from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
import jwt
from jwt import PyJWKClient
from config.config_file import OIDC_CONFIG

AUTH0_DOMAIN = OIDC_CONFIG['domain']
ALGORITHMS = OIDC_CONFIG['algorithms']
API_AUDIENCE = OIDC_CONFIG['audience']

# ใช้ HTTPBearer สำหรับรับ Bearer Token
oauth2_scheme = HTTPBearer()

def verify_token(authorization: str = Depends(oauth2_scheme)):
    token = authorization.credentials  # ดึง Bearer Token จาก header
    try:
        # แปลง token เป็น bytes
        token_bytes = token.encode('utf-8')

        # ดึง JWKS จาก Auth0
        JWKS_URL = f'https://{AUTH0_DOMAIN}/.well-known/jwks.json'
        jwks_client = PyJWKClient(JWKS_URL)
        signing_key = jwks_client.get_signing_key_from_jwt(token).key  # ดึง public key

        payload = jwt.decode(
            token_bytes,  # ใช้ token ที่เป็น bytes
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
