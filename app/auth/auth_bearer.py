from fastapi import HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from app.auth.hashing import decode_jwt, JWT_SECRET_KEY

class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        """Initialize JWTBearer with optional auto error handling."""
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        """Validate Bearer token from request and return token if valid."""
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if not credentials:
            raise HTTPException(status_code=403, detail="Invalid authorization code")
        if credentials.scheme != "Bearer":
            raise HTTPException(status_code=403, detail="Invalid authentication scheme")
        if not self.verify_jwt(credentials.credentials):
            raise HTTPException(status_code=403, detail="Invalid token or expired token")
        return credentials.credentials

    def verify_jwt(self, jwtoken: str) -> bool:
        """Verify if the JWT access token is valid using JWT_SECRET_KEY."""
        try:
            payload = decode_jwt(jwtoken, JWT_SECRET_KEY)
            return bool(payload)
        except:
            return 
        