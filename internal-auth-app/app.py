from fastapi import FastAPI, Header
from fastapi.responses import JSONResponse
import python_jwt as jwt
import jwcrypto.jwk as jwk
import datetime
import os
public_key_external = os.environ['JWT_PUBLIC_EXTERNAL']
private_key_internal = os.environ['JWT_PRIVATE_INTERNAL']
external_iss = 'demo.local'
external_sub = 'example'
internal_iss = 'cluster.local'
internal_sub = 'internal'
jwt_prefix = "Bearer "
internal_jwt_ttl_hours = 1


app = FastAPI()

@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"])
async def auth(path:str, authorization: str = Header(default=None)):
    """
    Convert Token: validate the received external JWT, and generate internal JWT
    This method must accept all HTTP verbs and paths
    """
    try:
        #print(f"Header: {str(authorization)}")
        if not authorization.startswith(jwt_prefix):
            return JSONResponse(status_code=401, headers=None, content="invalid token prefix")
        token = authorization[len(jwt_prefix):]

        external_header, external_claims = jwt.verify_jwt(token, jwk.JWK.from_json(public_key_external), ['RS256'])

        if external_claims['iss'] != external_iss or external_claims['sub'] != external_sub:
            return JSONResponse(status_code=401, headers=None, content="invalid token claims")
    except:
        return JSONResponse(status_code=401, headers=None, content="invalid token")

    try:
        # get user info from a source: external_claims['realm']
        # optionally check with the external auth server, to make sure user is still valid or possibly updated
        user_id = "1000"
        if external_claims['username'] == "demo":
            user_id = "1001"
        permission = "all"
        role = "developer"
        # generate the new internal JWT
        internal_raw_payload = {
            'iss': internal_iss,
            'sub': internal_sub,
            'permission': permission,
            'role': role,
            'user_id': user_id,
        }
        internal_jwt_token = jwt.generate_jwt(
            internal_raw_payload, jwk.JWK.from_json(private_key_internal), 'RS256', datetime.timedelta(hours=int(internal_jwt_ttl_hours)))

        headers = {"Authorization": jwt_prefix + internal_jwt_token}
        return JSONResponse(status_code=200, headers=headers, content=None)
    except:
        return JSONResponse(status_code=401, headers=None, content="not authorized")
