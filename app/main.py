from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_
from .database import get_db, engine
from . import models
from .schemas import Movie, CreateMovie, UpdateMovie

models.Base.metadata.create_all(bind=engine)

app = FastAPI()   

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3001", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/movies", response_model=List[Movie])
def findAll(search: Optional[str] = None, db: Session = Depends(get_db)):    
    if (search is None):
        return db.query(models.Movie).all()
        
    search = f"%{search.lower()}%"
    movies = db.query(models.Movie).filter(
        or_(
            models.Movie.name.ilike(search),
            models.Movie.description.ilike(search)
        )
    ).all()
    
    return movies

@app.get("/movies/{movie_id}", response_model=Movie)
def findOne(movie_id: int, db: Session = Depends(get_db)):
    db_movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()
    
    if (db_movie is None):
        raise HTTPException(404)
    
    return db_movie

@app.post("/movies", response_model=Movie)
def create(movie: CreateMovie, db: Session = Depends(get_db)):
    db_movie = models.Movie(**movie.model_dump())
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie

@app.put("/movies/{movie_id}", response_model=Movie)
def update(movie_id: int, movie: UpdateMovie, db: Session = Depends(get_db)):
    db_movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()
    
    if (db_movie is None):
        raise HTTPException(404)
    
    for key, value in movie.model_dump(exclude_unset=True).items():
        setattr(db_movie, key, value)
        
    db.commit()
    db.refresh(db_movie)
    
    return db_movie

@app.delete("/movies/{movie_id}", status_code=204)
def delete(movie_id: int, db: Session = Depends(get_db)):
    db_movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()
    
    if (db_movie is None):
        raise HTTPException(404)
    
    db.delete(db_movie)
    db.commit()
    
    return