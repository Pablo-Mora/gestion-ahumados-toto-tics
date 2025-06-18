from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./tic_assets.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db" # Example for PostgreSQL

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False} # Needed only for SQLite
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Function to create all tables
def create_db_and_tables():
    Base.metadata.create_all(bind=engine)
