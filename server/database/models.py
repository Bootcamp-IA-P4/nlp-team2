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
    updated_at = Column(DateTime, nullable=False)

    threads = relationship("Thread", back_populates="video", cascade="all, delete-orphan")
    requests = relationship("Request", back_populates="video", cascade="all, delete-orphan")


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
    comment = Column(Text)
    inserted_at = Column(DateTime, nullable=False)

    video = relationship("Video", back_populates="threads")
    request = relationship("Request", back_populates="threads")
    author_obj = relationship("Author", back_populates="threads")


class Author(Base):
    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    threads = relationship("Thread", back_populates="author_obj", cascade="all, delete-orphan")
