from datetime import datetime, timedelta
from typing import Any
from jose import jwt
import bcrypt
import os
from dotenv import load_dotenv
from fastapi import HTTPException

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7
ALGORITHM = "HS256"
JWT_SECRET_KEY = os.environ["JWT_SECRET_KEY"]
JWT_REFRESH_SECRET_KEY = os.environ["JWT_REFRESH_SECRET_KEY"]

def hash_password(password: str) -> str:
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY not found in .env file")
    peppered_password = (password + SECRET_KEY).encode('utf-8')
    # Hash with bcrypt
    hashed = bcrypt.hashpw(peppered_password, bcrypt.gensalt())
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY not found in .env file")
    # Add same pepper to plain password
    peppered_password = (plain_password + SECRET_KEY).encode('utf-8')
    return bcrypt.checkpw(peppered_password, hashed_password.encode('utf-8'))

"""JWT Token Creation and Decoding Functions
This module provides functions to create and decode JWT tokens for user authentication.
"""
def create_access_token(subject: str, expires_delta: timedelta = None) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(subject: str, expires_delta: timedelta = None) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_REFRESH_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_jwt(token: str, secret_key: str) -> Any:
    try:
        decoded_token = jwt.decode(token, secret_key, algorithms=[ALGORITHM])
        return decoded_token
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    