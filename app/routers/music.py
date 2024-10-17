# app/routers/music.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import schemas, models, dependencies, auth
from transformers import pipeline
import scipy.io.wavfile
import os

router = APIRouter(
    prefix="/music",
    tags=["music"]
)

# Initialize the MusicGen model using Hugging Face's pipeline
synthesizer = pipeline("text-to-audio", model="facebook/musicgen-small")

@router.post("/generate", response_model=schemas.MusicOut)
def generate_music(music: schemas.MusicCreate, db: Session = Depends(dependencies.get_db), current_user: models.User = Depends(auth.get_current_user)):
    try:
        # Use the MusicGen model to generate music from the prompt
        generated_music = synthesizer(music.prompt, forward_params={"do_sample": True})
        
        # Extract audio data and sampling rate
        audio_data = generated_music["audio"]
        sampling_rate = generated_music["sampling_rate"]
        
        # Save the generated audio as a .wav file
        music_filename = f"musicgen_{current_user.id}_{music.prompt}.wav"
        music_filepath = os.path.join("generated_music", music_filename)  # Ensure this directory exists
        scipy.io.wavfile.write(music_filepath, rate=sampling_rate, data=audio_data)

        # Save the music details in the database
        new_music = models.Music(
            prompt=music.prompt,
            music_url=music_filepath,  # Save the file path or a URL if you're storing the file in a cloud service
            owner_id=current_user.id
        )
        db.add(new_music)
        db.commit()
        db.refresh(new_music)

        return new_music

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate music: {str(e)}")


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