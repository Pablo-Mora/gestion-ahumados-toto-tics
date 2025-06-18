from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

# Import schemas for TokenData, User model
from . import schemas as auth_schemas
from . import models as auth_models # Renamed to avoid conflict
from app.crud import user as user_crud # Import user CRUD functions
from app.database import get_db # Import get_db dependency
import os
from dotenv import load_dotenv # Optional: for local .env file loading during development

load_dotenv() # Load .env file if present (for local development)

# SECURITY WARNING: In a production environment, SECRET_KEY MUST be set via an environment variable
# and should be a strong, randomly generated string.
# Do not use the default value in production.
# Example for generating a good key: openssl rand -hex 32
SECRET_KEY = os.getenv("SECRET_KEY", "a_very_insecure_default_secret_key_for_dev_only")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

if SECRET_KEY == "a_very_insecure_default_secret_key_for_dev_only" and os.getenv("APP_ENV") != "development":
    print("CRITICAL WARNING: Using default insecure SECRET_KEY in a non-development environment. This is UNSAFE.")
    # For a real production scenario, you might want to raise an error or exit:
    # raise ValueError("CRITICAL: SECRET_KEY is not set to a secure value in production.")
elif SECRET_KEY == "a_very_insecure_default_secret_key_for_dev_only":
     print("WARNING: Using default insecure SECRET_KEY. Suitable only for local development.")


# Define oauth2_scheme, tokenUrl should match the login route
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Placeholder: Function to get user from DB (dependency for protected routes)
async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> auth_models.User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = auth_schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception

    user = user_crud.get_user_by_username(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: auth_models.User = Depends(get_current_user)) -> auth_models.User:
    if not current_user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    return current_user

async def get_current_admin_user(current_user: auth_models.User = Depends(get_current_active_user)) -> auth_models.User:
    if current_user.role != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions. Admin role required."
        )
    return current_user
