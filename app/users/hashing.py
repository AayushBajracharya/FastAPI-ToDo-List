import bcrypt
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")

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
