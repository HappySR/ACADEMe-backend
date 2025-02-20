import firebase_admin
from firebase_admin import auth
from fastapi import HTTPException, Depends, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
import os
from datetime import datetime, timedelta
from passlib.context import CryptContext

# JWT Secret Key
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your_secret_key")

# Token expiry (30 days)
ACCESS_TOKEN_EXPIRE_MINUTES = 43200

# Password hashing setup
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Firebase authentication initialization
if not firebase_admin._apps:
    firebase_admin.initialize_app()

security = HTTPBearer()

def verify_firebase_token(token: str):
    """Verifies Firebase token."""
    try:
        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid Firebase token")

def create_jwt_token(data: dict):
    """Creates a JWT token with expiry."""
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    data.update({"exp": expire})
    return jwt.encode(data, JWT_SECRET_KEY, algorithm="HS256")

def verify_jwt_token(token: str):
    """Verifies and decodes a JWT token."""
    try:
        return jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

def get_current_user(credentials: HTTPAuthorizationCredentials = Security(security)):
    """Extracts the current user from JWT token."""
    token = credentials.credentials
    return verify_jwt_token(token)

def hash_password(password: str):
    """Hashes the password using bcrypt."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    """Verifies the password against the hashed version."""
    return pwd_context.verify(plain_password, hashed_password)
