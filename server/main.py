from fastapi import Depends, FastAPI
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
import os
from dotenv import load_dotenv

# Initialize FastAPI app
app = FastAPI()

# Load environment variables from .env file
load_dotenv()
DATABASE_URL = os.getenv("postgres_url")

# Create a connection to the database
engine = create_engine(DATABASE_URL)

# Create a session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

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
    # Extract the data from the request
    print(user.name)
    print(user.email)
    print(user.password)
    
    # TODO: Check if user already exists in db
    # TODO: Add user to db
    
    return {"message": "User created successfully"}