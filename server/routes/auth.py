from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import bcrypt
import uuid
from models.user import User
from pydantic_schemas.user_create import UserCreate
from fastapi import APIRouter
from database import get_db


router = APIRouter()

@router.post("/signup")
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