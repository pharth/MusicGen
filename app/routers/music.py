# app/routers/music.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, models, dependencies, auth
import os
from typing import List
import requests

router = APIRouter(
    prefix="/music",
    tags=["music"]
)

META_API_KEY = os.getenv("META_API_KEY")
META_API_URL = "https://api.meta.com/generate_music"  # Replace with actual Meta API endpoint

@router.post("/generate", response_model=schemas.MusicOut)
def generate_music(music: schemas.MusicCreate, db: Session = Depends(dependencies.get_db), current_user: models.User = Depends(auth.get_current_user)):
    # Call Meta API to generate music from prompt
    headers = {"Authorization": f"Bearer {META_API_KEY}"}
    payload = {"prompt": music.prompt}
    response = requests.post(META_API_URL, json=payload, headers=headers)
    
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Failed to generate music")
    
    data = response.json()
    music_url = data.get("music_url")  # Adjust based on Meta API response

    new_music = models.Music(
        prompt=music.prompt,
        music_url=music_url,
        owner_id=current_user.id
    )
    db.add(new_music)
    db.commit()
    db.refresh(new_music)
    return new_music

@router.post("/{music_id}/add_vocals", response_model=schemas.MusicOut)
def add_vocals(music_id: int, vocals_file: bytes, db: Session = Depends(dependencies.get_db), current_user: models.User = Depends(auth.get_current_user)):
    # Placeholder for adding vocals
    # Implement uploading vocals and integrating with the generated music
    music = db.query(models.Music).filter(models.Music.id == music_id, models.Music.owner_id == current_user.id).first()
    if not music:
        raise HTTPException(status_code=404, detail="Music not found")
    
    # Assume you have a service to handle vocals
    vocals_url = upload_vocals(vocals_file)  # Implement this function
    
    music.vocals_url = vocals_url
    db.commit()
    db.refresh(music)
    return music

@router.get("/", response_model=List[schemas.MusicOut])
def list_musics(db: Session = Depends(dependencies.get_db), current_user: models.User = Depends(auth.get_current_user)):
    musics = db.query(models.Music).filter(models.Music.owner_id == current_user.id).all()
    return musics

def upload_vocals(vocals_file: bytes) -> str:
    # Implement the actual upload logic, e.g., to AWS S3 or another storage service
    # For demonstration, return a dummy URL
    return "https://storage.service.com/vocals/your_vocals_file.mp3"
