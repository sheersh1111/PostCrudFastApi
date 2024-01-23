# models.py

from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
from typing import List  # Import List from typing module

DATABASE_URL = "postgresql://sheersh:bD3pdpve5wv8kia0bHHoyiQxECkqgAUw@dpg-cmnq2h0l5elc738nget0-a.oregon-postgres.render.com/postcrud"

Base = declarative_base()

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    body = Column(String)

# Create the database engine
engine = create_engine(DATABASE_URL)

# Create the table
Base.metadata.create_all(bind=engine)

# Pydantic model for validation and serialization
class PostCreate(BaseModel):
    title: str
    body: str

class PostResponse(BaseModel):
    id: int
    title: str
    body: str

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# SessionLocal class for database session management
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
