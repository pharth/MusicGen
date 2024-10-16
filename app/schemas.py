# app/schemas.py
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class MusicCreate(BaseModel):
    prompt: str

class MusicOut(BaseModel):
    id: int
    prompt: str
    music_url: Optional[str]
    vocals_url: Optional[str]
    created_at: datetime

    class Config:
        orm_mode = True
