# Pydantic and ORM models for jobs and subscribers
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from sqlalchemy import Column, Integer, String, DateTime, JSON, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

Base = declarative_base()

# Pydantic Models (para API validation)
class JobBase(BaseModel):
    title: str
    location: str = ""
    closing_date: str = ""
    requirements: str = ""
    url: str = ""

class JobCreate(JobBase):
    pass

class Job(JobBase):
    id: int
    detected_at: datetime
    
    class Config:
        from_attributes = True

class SubscriberBase(BaseModel):
    chat_id: str
    filters: dict = Field(default_factory=dict)

class SubscriberCreate(SubscriberBase):
    pass

class Subscriber(SubscriberBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class JobsResponse(BaseModel):
    jobs: List[Job]
    total: int

class SubscribeRequest(BaseModel):
    chat_id: str
    filters: dict = Field(default_factory=lambda: {"role": "Técnico en Sistemas", "location": "Valle del Cauca"})

class MonitoringRequest(BaseModel):
    filters: dict = Field(default_factory=lambda: {"role": "Técnico en Sistemas", "location": "Valle del Cauca"})

# SQLAlchemy Models (para database)
class JobModel(Base):
    __tablename__ = "jobs"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    location = Column(String, index=True)
    closing_date = Column(String)
    requirements = Column(String)
    url = Column(String, unique=True, index=True)  # Para evitar duplicados
    detected_at = Column(DateTime, default=datetime.utcnow)

class SubscriberModel(Base):
    __tablename__ = "subscribers"
    
    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(String, unique=True, index=True)
    filters = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./simo.db")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_tables():
    """Crear todas las tablas en la base de datos"""
    Base.metadata.create_all(bind=engine)

def get_db():
    """Dependency para obtener sesión de base de datos"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
