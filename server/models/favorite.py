from models.base import Base
from sqlalchemy import Column, ForeignKey, TEXT
from sqlalchemy.orm import relationship


class Favorite(Base):
    __tablename__ = 'favorites'

    id = Column(TEXT, primary_key=True)
    song_id = Column(TEXT, ForeignKey('song.id'))
    user_id = Column(TEXT, ForeignKey('users.id'))

    song = relationship("Song")
    user = relationship("User", back_populates="favorites")
