from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
import os

# Security configuration - MUST be set via environment variables
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("SECRET_KEY environment variable is not set! Generate one with: python3 -c 'import secrets; print(secrets.token_urlsafe(32))'")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

# Password hashing
try:
    pwd_context = CryptContext(
        schemes=["bcrypt"], deprecated="auto", bcrypt__default_rounds=12)
except Exception as e:
    # Fallback to a simpler scheme if bcrypt has issues
    pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")

# Security scheme
security = HTTPBearer()


class TokenData(BaseModel):
    username: Optional[str] = None


def verify_password(plain_password, hashed_password):
    """Verify a password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    """Hash a password."""
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify JWT token."""
    try:
        payload = jwt.decode(credentials.credentials,
                             SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return TokenData(username=username)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


# Admin user credentials from environment variables
def _get_admin_users():
    """Load admin users from environment variables."""
    admin_username = os.getenv("ADMIN_USERNAME", "admin")
    admin_password = os.getenv("ADMIN_PASSWORD")

    if not admin_password:
        raise ValueError("ADMIN_PASSWORD environment variable is not set! This is required for security.")

    # Hash the password from environment variable
    hashed_password = get_password_hash(admin_password)

    return {
        admin_username: {
            "username": admin_username,
            "hashed_password": hashed_password,
            "full_name": "Administrator",
            "disabled": False,
        }
    }


def authenticate_user(username: str, password: str):
    """Authenticate a user."""
    admin_users = _get_admin_users()
    user = admin_users.get(username)
    if not user:
        return False
    # Verify against the environment variable password directly for consistency
    admin_password = os.getenv("ADMIN_PASSWORD")
    if password != admin_password:
        return False
    return user
