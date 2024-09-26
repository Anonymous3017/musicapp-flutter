from fastapi import FastAPI
from database import engine
from models.base import Base
from routes import auth

# Initialize FastAPI app
app = FastAPI()

# Include the auth router
app.include_router(auth.router, prefix="/auth")

# Create all tables
Base.metadata.create_all(bind=engine)