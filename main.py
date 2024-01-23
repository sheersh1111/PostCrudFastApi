# main.py

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Post, Base , engine,PostCreate, PostResponse
from typing import List
app = FastAPI()

# Create the tables
Base.metadata.create_all(bind=engine)


# Create a post
@app.post("/posts", response_model=PostResponse)
def create_post(post: PostCreate, db: Session = Depends(get_db)):
    db_post = Post(**post.dict())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

# Get all posts
@app.get("/posts", response_model=List[PostResponse])
def read_posts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    posts = db.query(Post).offset(skip).limit(limit).all()
    return posts

# Get a single post by its ID
@app.get("/posts/{post_id}", response_model=PostResponse)
def read_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

# Update a post by its ID
@app.put("/posts/{post_id}", response_model=PostResponse)
def update_post(post_id: int, post_update: PostCreate, db: Session = Depends(get_db)):
    db_post = db.query(Post).filter(Post.id == post_id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    
    for field, value in post_update.dict().items():
        setattr(db_post, field, value)
    
    db.commit()
    db.refresh(db_post)
    return db_post

# Delete a post by its ID
@app.delete("/posts/{post_id}", response_model=None)
def delete_post(post_id: int, db: Session = Depends(get_db)):
    db_post = db.query(Post).filter(Post.id == post_id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    
    db.delete(db_post)
    db.commit()
    return {'success':True,'message':'Post Deleted Successfully'}