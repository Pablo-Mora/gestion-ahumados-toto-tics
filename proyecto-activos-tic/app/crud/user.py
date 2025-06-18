from sqlalchemy.orm import Session

from app.auth import models as auth_models # Alias to avoid confusion if other models exist
from app.auth import schemas as auth_schemas # Alias for clarity
from app.auth.auth import get_password_hash # Import the actual hashing function

def get_user_by_username(db: Session, username: str):
    return db.query(auth_models.User).filter(auth_models.User.username == username).first()

def get_user_by_email(db: Session, email: str): # Good to have for checking existing email
    return db.query(auth_models.User).filter(auth_models.User.email == email).first()

def create_user(db: Session, user: auth_schemas.UserCreate) -> auth_models.User:
    hashed_password = get_password_hash(user.password)
    db_user = auth_models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        full_name=user.full_name, # Ensure UserCreate schema has this if used
        role=user.role,
        is_active=True # Default to active on creation
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
