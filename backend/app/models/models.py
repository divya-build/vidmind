from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.database import Base

# ─── Status Enums ───────────────────────────────────────────
class VideoStatus(enum.Enum):
    pending   = "pending"
    scripting = "scripting"
    imaging   = "imaging"
    audio     = "audio"
    assembling = "assembling"
    done      = "done"
    failed    = "failed"

class AssetType(enum.Enum):
    image = "image"
    audio = "audio"

# ─── User Table ─────────────────────────────────────────────
class User(Base):
    __tablename__ = "users"

    id         = Column(Integer, primary_key=True, index=True)
    email      = Column(String(255), unique=True, nullable=False)
    password   = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    videos = relationship("Video", back_populates="user")

# ─── Video Table ─────────────────────────────────────────────
class Video(Base):
    __tablename__ = "videos"

    id         = Column(Integer, primary_key=True, index=True)
    user_id    = Column(Integer, ForeignKey("users.id"), nullable=False)
    title      = Column(String(255), nullable=False)
    prompt     = Column(Text, nullable=False)
    script     = Column(Text, nullable=True)
    status     = Column(Enum(VideoStatus), default=VideoStatus.pending)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user   = relationship("User", back_populates="videos")
    scenes = relationship("Scene", back_populates="video")

# ─── Scene Table ─────────────────────────────────────────────
class Scene(Base):
    __tablename__ = "scenes"

    id           = Column(Integer, primary_key=True, index=True)
    video_id     = Column(Integer, ForeignKey("videos.id"), nullable=False)
    scene_number = Column(Integer, nullable=False)
    description  = Column(Text, nullable=True)
    narration    = Column(Text, nullable=True)
    created_at   = Column(DateTime, default=datetime.utcnow)

    video  = relationship("Video", back_populates="scenes")
    assets = relationship("Asset", back_populates="scene")

# ─── Asset Table ─────────────────────────────────────────────
class Asset(Base):
    __tablename__ = "assets"

    id         = Column(Integer, primary_key=True, index=True)
    scene_id   = Column(Integer, ForeignKey("scenes.id"), nullable=False)
    type       = Column(Enum(AssetType), nullable=False)
    file_path  = Column(String(500), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    scene = relationship("Scene", back_populates="assets")