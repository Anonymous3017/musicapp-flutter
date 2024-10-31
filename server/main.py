from fastapi import FastAPI
import uvicorn
from database import engine
from models.base import Base
from routes import auth, song

# Initialize FastAPI app
app = FastAPI()

# Include the auth router
app.include_router(auth.router, prefix="/auth")
app.include_router(song.router, prefix="/song")

# Create all tables
Base.metadata.create_all(bind=engine)