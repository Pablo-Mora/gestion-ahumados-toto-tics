from sqlalchemy import Boolean, Column, Integer, String
from app.database import Base # Import Base from app.database

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False) # Made email non-nullable
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="USER", nullable=False) # e.g., 'USER', 'ADMIN'
    is_active = Column(Boolean, default=True) # Renamed from 'disabled' and inverted logic

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}', role='{self.role}', is_active={self.is_active})>"
