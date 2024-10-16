# app/main.py
from fastapi import FastAPI
from .database import engine, Base
from .routers import users, music

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Music Generation App",
    description="Generate music from text, add vocals, and save your creations.",
    version="1.0.0"
)

app.include_router(users.router)
app.include_router(music.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Music Generation App!"}
