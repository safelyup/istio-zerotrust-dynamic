from fastapi import FastAPI
from pydantic import BaseModel
import python_jwt as jwt
import jwcrypto.jwk as jwk
import datetime
import os
external_private_key = os.environ['JWT_PRIVATE_EXTERNAL']

app = FastAPI()

class JWT(BaseModel):
    token: str

class TokenPayLoad(BaseModel):
    username: str

@app.post("/token")
async def gen_token(payload:TokenPayLoad):
    """
    Generate Token: return a JWT token, valid for 1 hour
    """
    if not len(payload.username):
        return "username is required"

    raw_payload = {
        'iss': 'demo.local',
        'sub': 'example',
        'realm': 'customer',
        'username': payload.username
    }
    jwt_token = jwt.generate_jwt(
        raw_payload, jwk.JWK.from_json(external_private_key), 'RS256', datetime.timedelta(hours=1))
    return jwt_token
