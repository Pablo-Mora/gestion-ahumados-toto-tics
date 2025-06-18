from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

from sqlalchemy.orm import Session

from . import schemas, auth, models as auth_models # Pydantic models, Auth logic and auth_models for type hint
# from . import models # SQLAlchemy models (User model is accessed via auth.get_current_active_user or user_crud)
from app.database import get_db
from app.crud import user as user_crud # User CRUD operations

router = APIRouter(
    prefix="/auth", # Ensure this prefix is used in main.py
    tags=["Authentication"],
)

@router.post("/token", response_model=schemas.Token)
async def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = user_crud.get_user_by_username(db, username=form_data.username)
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/users/", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
async def create_new_user(
    user_to_create: schemas.UserCreate,
    db: Session = Depends(get_db),
    admin_user: auth_models.User = Depends(auth.get_current_admin_user) # Protect route
):
    # admin_user is available here if needed for logging or specific logic
    # The route is protected by the dependency itself.

    # Note: To create the first admin user, you might need to:
    # 1. Temporarily remove admin protection (Depends(auth.get_current_admin_user)) from this route,
    #    register the admin, then add protection back.
    # 2. Or, use a separate script to insert an admin user directly into the database.
    # Example for script (conceptual, ensure imports and Base are correct if used standalone):
    # from app.database import SessionLocal, Base, engine
    # from app.auth.models import User as AuthUser # Alias to avoid confusion
    # from app.auth.auth import get_password_hash
    # AuthUser.metadata.create_all(bind=engine) # Ensure table exists if run standalone
    # db_script = SessionLocal()
    # admin_user_script = AuthUser(username="admin", email="admin@example.com", hashed_password=get_password_hash("adminpassword"), role="ADMIN", is_active=True)
    # db_script.add(admin_user_script)
    # db_script.commit()
    # print("Admin user created")
    # db_script.close()

    db_user_by_username = user_crud.get_user_by_username(db, username=user_to_create.username)
    if db_user_by_username:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")

    db_user_by_email = user_crud.get_user_by_email(db, email=user_to_create.email)
    if db_user_by_email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    created_user = user_crud.create_user(db=db, user=user_to_create)
    # Return type is schemas.User, which should not include hashed_password
    # Pydantic's orm_mode will handle the conversion from the SQLAlchemy model
    return created_user

# Example of a protected route
@router.get("/users/me", response_model=schemas.User)
async def read_users_me(current_user: auth_models.User = Depends(auth.get_current_active_user)): # Corrected type hint
    # current_user is already a User model instance from get_current_active_user
    # Pydantic will convert it to schemas.User for the response
    return current_user
