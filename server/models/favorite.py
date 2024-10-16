from models.base import Base
from sqlalchemy import Column, ForeignKey, TEXT


class Favorite(Base):
    __tablename__ = 'favorites'

    id = Column(TEXT, primary_key=True)
    song_id = Column(TEXT, ForeignKey('song.id'))
    user_id = Column(TEXT, ForeignKey('users.id'))
