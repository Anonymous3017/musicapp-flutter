import os
import uuid
import cloudinary
import cloudinary.uploader
from fastapi import APIRouter, Depends, File, Form, UploadFile
from sqlalchemy.orm import Session
from database import get_db
from middleware.auth_middleware import auth_middleware
from dotenv import load_dotenv
from models.song import Song
from pydantic_schemas.favorite_song import FavoriteSong
from models.favorite import Favorite



router = APIRouter()
load_dotenv()

# Configuration       
cloudinary.config( 
    cloud_name = "ds61kwof5", 
    api_key = "592577737874135", 
    api_secret = os.getenv("CLOUDINARY_SECRET_KEY"),
    secure=True
)

@router.post("/upload", status_code=201)
def upload_song(song: UploadFile = File(...), 
                thumbnail: UploadFile = File(...),
                artist: str = Form(...), 
                song_name: str = Form(...), 
                hex_code: str = Form(...),
                db: Session = Depends(get_db),
                auth_dict = Depends(auth_middleware)):
    
    # Upload song to cloudinary

    song_id = str(uuid.uuid4())
    song_res = cloudinary.uploader.upload(song.file, resource_type='auto' ,folder=f"songs/{song_id}")
    #for thumbnauil
    thumbnail_res = cloudinary.uploader.upload(thumbnail.file, resource_type='image' ,folder=f"songs/{song_id}")

    new_song = Song(
        id = song_id,
        song_url = song_res['url'],
        thumbnail_url = thumbnail_res['url'],
        artist = artist,
        song_name = song_name,
        hex_code = hex_code
    )

    db.add(new_song)
    db.commit()
    db.refresh(new_song)

    return new_song

@router.get("/list")
def list_songs(db: Session = Depends(get_db), auth_dict = Depends(auth_middleware)):
    songs = db.query(Song).all()
    return songs

@router.post("/favorite")
def favorite_song(song: FavoriteSong, 
                  db: Session = Depends(get_db), 
                  auth_dict = Depends(auth_middleware),):
    #song is already favorited by the user
    user_id = auth_dict['uid']

    fav_song = db.query(Favorite).filter(Favorite.song_id == song.song_id, Favorite.user_id == user_id).first()

    if fav_song:
    # if the song is already favorited by the user, unfavorite it
        db.delete(fav_song)
        db.commit()
        return {"message": False}
    #if the song is not favorited by the user, favorite it
    else:
        new_fav = Favorite(
            id=str(uuid.uuid4()),
            song_id = song.song_id,
            user_id = user_id
        )
        db.add(new_fav)
        db.commit()
        db.refresh(new_fav)
        return {"message": True}
