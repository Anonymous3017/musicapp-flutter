import os
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import bcrypt
import uuid
from models.user import User
from pydantic_schemas.user_create import UserCreate
from fastapi import APIRouter
from database import get_db
from pydantic_schemas.user_login import UserLogin
import jwt
from dotenv import load_dotenv


router = APIRouter()
load_dotenv()

@router.post("/signup", status_code=status.HTTP_201_CREATED)
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

    return user_db

@router.post("/login")
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    #check if a user with same email already exists
    user_db = db.query(User).filter(User.email == user.email).first()

    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid credentials"
        )
    #password matching or not
    if not bcrypt.checkpw(user.password.encode(), user_db.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid credentials"
        )
    
    #generate jwt token
    jwt_token = jwt.encode({"id": user_db.id }, os.getenv("JWT_SECRET_KEY"))

    return {"token": jwt_token, "user": user_db}