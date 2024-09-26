from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, String, LargeBinary, TEXT, VARCHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import os
from dotenv import load_dotenv
import bcrypt
import uuid

# Initialize FastAPI app
app = FastAPI()

# Load environment variables from .env file
load_dotenv()
DATABASE_URL = os.getenv("postgres_url")

# Create a connection to the database
engine = create_engine(DATABASE_URL)

# Create a session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base model for SQLAlchemy
Base = declarative_base()

# Create a user table
class User(Base):
    __tablename__ = "users"
    id = Column(TEXT, primary_key=True, index=True)
    name = Column(VARCHAR, index=True)
    email = Column(VARCHAR, unique=True, index=True)
    password = Column(LargeBinary)

# Create all tables
Base.metadata.create_all(bind=engine)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic model for user creation
class UserCreate(BaseModel):
    name: str
    email: str
    password: str

@app.post("/signup")
def signup_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Endpoint to sign up a new user.

    Args:
        user (UserCreate): The user data from the request body.
        db (SessionLocal): The database session.

    Returns:
        dict: A message indicating the user was created successfully.
    """
    # Check if email already exists
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )

    # Hash the password
    hash_password = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt())
    
    # Create a new user instance
    user_db = User(id=str(uuid.uuid4()), name=user.name, email=user.email, password=hash_password)
    
    # Add user to db
    db.add(user_db)
    db.commit()
    db.refresh(user_db)

    return {"message": "User created successfully"}