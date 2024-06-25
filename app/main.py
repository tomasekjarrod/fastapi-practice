from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from pydantic import BaseModel
import os
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = FastAPI()   

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3001", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = create_engine(os.getenv("DATABASE_URL"))

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class Movie(BaseModel):
    id: int
    name: str
    description: str
    rating: float
    
movies = {
    1:  Movie(id=1, name="Inception", rating=8.8, description="A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a CEO." ),
    2:  Movie(id=2, name="The Dark Knight", rating=9.0, description="When the menace known as the Joker emerges from his mysterious past, he wreaks havoc and chaos on the people of Gotham."),
    3:  Movie(id=3, name="Interstellar", rating=8.6, description="A team of explorers travel through a wormhole in space in an attempt to ensure humanity's survival."),
    4:  Movie(id=4, name="Comeback Kids", rating=6.6, description="Reload server please")
}

@app.get("/movies", response_model=List[Movie])
def findAll(search: Optional[str] = None, db: Session = Depends(get_db)):    
    if (search is None):
        return movies.values()
    
    return list(filter(lambda movie: search.lower() in movie.name.lower(), movies.values()))

@app.get("/movies/{movie_id}", response_model=Movie)
def findOne(movie_id: int):
    if (movie_id not in movies):
        raise HTTPException(404, "Movie not found")
    
    return movies[movie_id]

@app.post("/movies", response_model=Movie)
def create(movie: Movie):
    if (movie.id in movies):
        raise HTTPException(422, "Id {} already exists in movies".format(movie.id))
    
    movies[movie.id] = movie
    return movie

@app.put("/movies/{movie_id}", response_model=Movie)
def update(movie_id: int, rating: Optional[float] = None, description: Optional[str] = None):
    if (movie_id not in movies):
        raise HTTPException(404, "Movie not found")
    
    movie = movies[movie_id]
    
    if (rating is not None):
        movie.rating = rating
    if (description is not None):
        movie.description = description
        
    movies[movie.id] = movie
    
    return movie

@app.delete("/movies/{movie_id}", status_code=204)
def delete(movie_id: int):
    if (movie_id not in movies):
        raise HTTPException(404, "Movie not found")
    
    del movies[movie_id]
    
    return