from sqlalchemy import Column, Integer, String, Float, ForeignKey
from .database import Base
from sqlalchemy.orm import relationship

class Movie(Base):
    __tablename__ = "movies"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    rating = Column(Float)
    # director_id = Column(Integer, ForeignKey('directors.id'))
    # director = relationship("Director", back_populates="movies")
    
# class Director(Base):
#     __tablename__ = 'directors'
    
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String)
#     movies = relationship("Movie", back_populates="director")