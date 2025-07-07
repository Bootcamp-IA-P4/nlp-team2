from sqlalchemy import create_engine, Column, Float, Integer, DateTime, String, Text, ForeignKey, JSON, Boolean
from sqlalchemy.dialects.postgresql import JSONB  # si aún no lo has hecho
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime

Base = declarative_base()

class Video(Base):
    __tablename__ = 'videos'

    id = Column(Integer, primary_key=True)
    youtube_video_id = Column(String, unique=True, nullable=False)
    video_url = Column(String, nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text)
    fk_author_id = Column(Integer, ForeignKey('authors.id'))
    total_threads = Column(Integer)
    updated_at = Column(DateTime, nullable=False)

    total_likes = Column(Integer, nullable=True)
    total_comments = Column(Integer, nullable=True)
    emoji_stats = Column(JSONB, nullable=True)
    total_emojis = Column(Integer, nullable=True)
    most_common_emojis = Column(JSONB, nullable=True)

    threads = relationship("Thread", back_populates="video", cascade="all, delete-orphan")
    requests = relationship("Request", back_populates="video", cascade="all, delete-orphan")
    authors = relationship("Author", back_populates="videos")


class Request(Base):
    __tablename__ = 'requests'

    id = Column(Integer, primary_key=True)
    fk_video_id = Column(Integer, ForeignKey('videos.id'), nullable=False)
    request_date = Column(DateTime, nullable=False)

    video = relationship("Video", back_populates="requests")
    threads = relationship("Thread", back_populates="request", cascade="all, delete-orphan")


class Thread(Base):
    __tablename__ = 'threads'

    id = Column(Integer, primary_key=True)
    fk_video_id = Column(Integer, ForeignKey('videos.id'), nullable=False)
    fk_request_id = Column(Integer, ForeignKey('requests.id'), nullable=False)
    fk_author_id = Column(Integer, ForeignKey('authors.id'), nullable=True)
    parent_comment_id = Column(Integer, ForeignKey('threads.id'), nullable=True)
    comment = Column(Text)
    inserted_at = Column(DateTime, nullable=False)

    likes = Column(Integer, default=0)
    published_time = Column(String)
    emoji_count = Column(Integer, default=0)
    emojis = Column(JSON)
    has_replies = Column(Boolean, default=False)
    replies_count = Column(Integer, default=0)

    video = relationship("Video", back_populates="threads")
    request = relationship("Request", back_populates="threads")
    author_obj = relationship("Author", back_populates="threads")

class Author(Base):
    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    threads = relationship("Thread", back_populates="author_obj", cascade="all, delete-orphan")
    videos = relationship("Video", back_populates="authors", cascade="all, delete-orphan")



class VideoToxicitySummary(Base):
    __tablename__ = "video_toxicity_summary"

    id = Column(Integer, primary_key=True)
    fk_video_id = Column(Integer, ForeignKey("videos.id", ondelete="CASCADE"))
    fk_request_id = Column(Integer, ForeignKey("requests.id", ondelete="CASCADE"))
    total_comments = Column(Integer, nullable=False)
    toxic_comments = Column(Integer, nullable=False)
    toxicity_rate = Column(Float(5, 4), nullable=False)
    categories_summary = Column(JSON)
    most_toxic_thread_id = Column(Integer, ForeignKey("threads.id"))
    average_toxicity = Column(Float(5, 4))
    model_info = Column(JSON)
    analysis_completed_at = Column(DateTime, default=datetime.utcnow)

    video = relationship("Video", backref="toxicity_summary")
    request = relationship("Request", backref="toxicity_summary")
    most_toxic_thread = relationship("Thread", foreign_keys=[most_toxic_thread_id])

class ToxicityAnalysis(Base):
    __tablename__ = "toxicity_analysis"

    id = Column(Integer, primary_key=True)
    fk_thread_id = Column(Integer, ForeignKey("threads.id", ondelete="CASCADE"))
    fk_request_id = Column(Integer, ForeignKey("requests.id", ondelete="CASCADE"))
    is_toxic = Column(Boolean, nullable=False)
    toxicity_confidence = Column(Float(5, 4), nullable=False)
    categories_detected = Column(JSON)
    category_scores = Column(JSON)
    model_version = Column(String(20), default="1.0.0")
    analyzed_at = Column(DateTime, default=datetime.utcnow)

    thread = relationship("Thread", backref="toxicity_analysis", uselist=False)
    request = relationship("Request", backref="toxicity_analysis")
