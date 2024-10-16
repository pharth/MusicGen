# app/models.py
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    musics = relationship("Music", back_populates="owner")

class Music(Base):
    __tablename__ = "musics"

    id = Column(Integer, primary_key=True, index=True)
    prompt = Column(String, nullable=False)
    music_url = Column(String, nullable=True)
    vocals_url = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="musics")
