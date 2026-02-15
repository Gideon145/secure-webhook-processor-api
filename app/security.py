import hmac
import hashlib
import os

from fastapi import HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import jwt

SECRET_KEY = "supersecret"
JWT_SECRET = os.getenv("JWT_SECRET", "superjwtsecret")
JWT_ALGORITHM = "HS256"

bearer_scheme = HTTPBearer()


def verify_signature(payload: bytes, signature: str) -> bool:
    digest = hmac.new(SECRET_KEY.encode("utf-8"), payload, hashlib.sha256).hexdigest()
    return hmac.compare_digest(digest, signature)


def get_current_user(credentials: HTTPAuthorizationCredentials = bearer_scheme):
    token = credentials.credentials
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )
