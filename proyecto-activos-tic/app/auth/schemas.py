from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str
    role: str = "USER"  # Default role, can be changed by admin during creation by an admin

class UserLogin(BaseModel):
    username: str
    password: str

class User(UserBase):
    id: int
    disabled: Optional[bool] = None

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
