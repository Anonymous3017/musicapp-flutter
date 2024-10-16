from models.base import Base
from sqlalchemy import create_engine, Column, LargeBinary, TEXT, VARCHAR
from sqlalchemy.orm import relationship

# Create a user table
class User(Base):
    __tablename__ = "users"
    id = Column(TEXT, primary_key=True, index=True)
    name = Column(VARCHAR, index=True)
    email = Column(VARCHAR, unique=True, index=True)
    password = Column(LargeBinary)

    favorites = relationship("Favorite", back_populates="user")