from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()

class Video(Base):
    __tablename__ = 'videos'

    id = Column(Integer, primary_key=True)
    youtube_video_id = Column(String, unique=True, nullable=False)
    video_url = Column(String, nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text)
    author = Column(String)
    total_threads = Column(Integer)
    inserted_at = Column(DateTime, nullable=False)

    comments = relationship("Thread", back_populates="video", cascade="all, delete-orphan")


class Thread(Base):
    __tablename__ = 'threads'

    id = Column(Integer, primary_key=True)
    fk_video_id = Column(Integer, ForeignKey('videos.id'), nullable=False)
    author = Column(String)
    comment = Column(Text)
    inserted_at = Column(DateTime, nullable=False)

    video = relationship("Video", back_populates="comments")
